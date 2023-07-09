import datetime
import map_renderer

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from aiogram import Bot, Dispatcher, executor, types
from Backend.ObjectModels.user_request import UserRequest
from keyboards import get_start_kb, get_filter_kb, get_ans_list_kb, calendar, \
    get_confirmation_children_kb, start_searching_kb

meal_types = ["без питания", "завтрак", "завтрак+обед/ужин", "завтрак+обед+ужин", "всё включено"]
services = ["wifi", "парковка", "бассейн", "кондиционер", "с животными", "трансфер", "бар/ресторан"]
stars = ["Без звезд", "1 звезда", "2 звезды", "3 звезды", "4 звезды", "5 звезд"]

in_proses = {}
context_dict = {}

API_TOKEN = '5903687838:AAFciAPwabn0gSzfejp-YCkeaHOdeA9O2zI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if context_dict.get(message.from_user.id) is not None:
        await message.answer('Закончите заполнять запрос')
        return

    in_proses[message.from_user.id] = (UserRequest(message.from_user.id))
    context_dict[message.from_user.id] = "start"
    await message.answer('Здравствуйте, начнем работу', reply_markup=get_start_kb())


@dp.callback_query_handler(text="start")
async def add_filters_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "start"
    await callback.message.answer("Добавьте фильтры или начните поиск", reply_markup=get_start_kb())


@dp.callback_query_handler(text="add_filters")
async def add_filters_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "add_filters"
    await callback.message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[callback.from_user.id]))


@dp.callback_query_handler(text="date_check-in")
async def date_check_in_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "date_check-in"
    await callback.message.answer("Введите дату заезда: ", reply_markup=calendar)


@dp.callback_query_handler(text="date_check-out")
async def date_check_out_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "date_check-out"
    await callback.message.answer("Введите дату выезда: ", reply_markup=calendar)


@dp.callback_query_handler(text="adults_number")
async def adults_number_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "adults_number"
    await callback.message.answer("Введите количество взрослых: ")


@dp.callback_query_handler(text="children_ages")
async def children_ages_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "children_ages"
    await callback.message.answer("Введите возраст ребенка: ")


@dp.callback_query_handler(text="stars_number")
async def stars_number_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "stars_number"
    await callback.message.answer("Выберите количество звезд: ", reply_markup=get_ans_list_kb(stars))


@dp.callback_query_handler(text="price")
async def price_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "price"
    await callback.message.answer("Введите желаемый диапазон цен через дефиз \nПример: 100-10000 ")


@dp.callback_query_handler(text="meal_type")
async def meal_type_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "meal_type"
    await callback.message.answer("Добавьте тип питания: ", reply_markup=get_ans_list_kb(meal_types))


@dp.callback_query_handler(text="services")
async def services_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "services"
    await callback.message.answer("Добавьте доп сервисы: ", reply_markup=get_ans_list_kb(services))


@dp.callback_query_handler(text="finish")
async def handle_location(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "finish"
    await callback.message.answer("Введите радиус поиска в км: ")


@dp.callback_query_handler()
async def cal(callback: types.CallbackQuery):
    result, key, step = DetailedTelegramCalendar().process(callback.data)
    if not result and key:
        await callback.message.edit_reply_markup(reply_markup=key)
    elif result:
        if context_dict[callback.from_user.id] == "date_check-in":
            in_proses[callback.from_user.id].date_in = datetime.datetime.strptime(str(result),
                                                                                  '%Y-%m-%d').date()
        elif context_dict[callback.from_user.id] == "date_check-out":
            in_proses[callback.from_user.id].date_out = datetime.datetime.strptime(str(result),
                                                                                   '%Y-%m-%d').date()
        context_dict[callback.from_user.id] = "add_filters"
        await callback.message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[callback.from_user.id]))


@dp.message_handler()
async def data_message_handler(message: types.Message):
    context = context_dict[message.from_user.id]
    if context == "adults_number":
        in_proses[message.from_user.id].adults = int(message.text)
        await message.answer("Выбирите фильтры", reply_markup=get_filter_kb(in_proses[message.from_user.id]))
        context_dict[message.from_user.id] = "add_filters"

    elif context == "children_ages":
        in_proses[message.from_user.id].children_ages.append(int(message.text))
        await message.answer("Хотите добавить еще?", reply_markup=get_confirmation_children_kb())

    elif context == "price":
        in_proses[message.from_user.id].price = message.text
        await message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[message.from_user.id]))
        context_dict[message.from_user.id] = "add_filters"

    elif context == "meal_type":
        if in_proses[message.from_user.id].meal_types.count(message.text) == 1:
            in_proses[message.from_user.id].meal_types.remove(message.text)
        elif message.text == "Закончить":
            await message.answer(text="Фильтры добавлены", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[message.from_user.id]))
            context_dict[message.from_user.id] = "add_filters"
        else:
            in_proses[message.from_user.id].meal_types.append(message.text)

    elif context == "stars_number":

        if message.text == "Закончить":
            await message.answer(text="Фильтры добавлены", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[message.from_user.id]))
            context_dict[message.from_user.id] = "add_filters"
            return

        st = message.text.split(" ")[0]
        if st == "Без":
            st = "0"
        num = int(st)
        if in_proses[message.from_user.id].stars.count(num) == 1:
            in_proses[message.from_user.id].stars.remove(num)
        else:
            in_proses[message.from_user.id].stars.append(num)

    elif context == "finish":
        in_proses[message.from_user.id].radius_km = int(message.text)
        await message.answer("Тут будут выводится отели", reply_markup=start_searching_kb)
        pass

    elif context == "services":
        if in_proses[message.from_user.id].services.count(message.text) == 1:
            in_proses[message.from_user.id].services.remove(message.text)
        elif message.text == "Закончить":
            await message.answer(text="Фильтры добавлены", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[message.from_user.id]))
            context_dict[message.from_user.id] = "add_filters"
        else:
            in_proses[message.from_user.id].services.append(message.text)

    elif context == "finish":
        in_proses[message.from_user.id].radius_km = int(message.text)
        await message.answer("Тут будут выводится отели", reply_markup=start_searching_kb)
        pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
