import datetime

from geopy import Nominatim

import map_renderer

from Backend.parsers.parser_101 import Parser101Hotels
from Backend.parsers.ostrovok_parser import OstrovokParser
from telegram_bot_calendar import DetailedTelegramCalendar
from Backend.DAOs.favorite_DAO import favorite_DAO
from Backend.DAOs.hotel_DAO import hotel_DAO
from Backend.DAOs.user_DAO import user_DAO
from Backend.DAOs.user_request_DAO import user_request_DAO
from aiogram import Bot, Dispatcher, executor, types
from Backend.ObjectModels.user_request import UserRequest
from Backend.ObjectModels.user import User
from Backend.ObjectModels.hotel import Hotel
from Backend.ObjectModels.favorite import favorite
from Backend.parserexecutor import ParserExecutor
from keyboards import get_start_kb, get_filter_kb, get_ans_list_kb, calendar, \
    get_confirmation_children_kb, get_admin_kb, get_welcome_kb, get_account_opt_kb, \
    get_back_kb

meal_types = ["без питания", "завтрак", "завтрак+обед/ужин", "завтрак+обед+ужин", "всё включено"]
services = ["wifi", "парковка", "бассейн", "кондиционер", "с животными", "трансфер", "бар/ресторан"]
stars = ["Без звезд", "1 звезда", "2 звезды", "3 звезды", "4 звезды", "5 звезд"]

in_proses = {}
context_dict = {}

usr_dao = user_DAO()
fav_dao = favorite_DAO()
htl_dao = hotel_DAO()
req_dao = user_request_DAO()

exectr = ParserExecutor([Parser101Hotels(), OstrovokParser])
API_TOKEN = '5903687838:AAFciAPwabn0gSzfejp-YCkeaHOdeA9O2zI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if not usr_dao.exist(message.from_user.id):
        usr_dao.add(User(message.from_user.id, message.from_user.username))

    context_dict[message.from_user.id] = "welcome"
    await message.answer('Здравствуйте, начнем работу',
                         reply_markup=get_welcome_kb(usr_dao.get_by_pk(message.from_user.id)))


@dp.callback_query_handler(text="welcome")
async def add_filters_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "welcome"
    await callback.message.answer('Начнем работу',
                                  reply_markup=get_welcome_kb(usr_dao.get_by_pk(callback.from_user.id)))


@dp.callback_query_handler(text="personal_account")
async def add_filters_handler(callback: types.CallbackQuery):
    usr = usr_dao.get_by_pk(callback.from_user.id)
    await callback.message.answer(str(usr), reply_markup=get_account_opt_kb())


@dp.callback_query_handler(text="favorites")
async def add_filters_handler(callback: types.CallbackQuery):
    msg = ''
    for fav in fav_dao.get_user_favorite(callback.from_user.id):
        msg = msg + str(htl_dao.get_by_pk(fav.hotel_name, fav.hotel_adderss)) + "\n\n"
    if msg == '':
        msg = "Нет избранных отелей"
    await callback.message.answer(msg, reply_markup=get_back_kb('personal_account'))


@dp.callback_query_handler(text="history")
async def add_filters_handler(callback: types.CallbackQuery):
    msg = ''
    for his in req_dao.get_by_user_id(callback.from_user.id):
        msg = msg + str(his) + "\n\n"
    if msg == '':
        msg = "Нет истории поиска"
    await callback.message.answer(msg, reply_markup=get_back_kb('personal_account'))


@dp.callback_query_handler(text="admin")
async def date_check_in_handler(callback: types.CallbackQuery):
    await callback.message.answer(f"здравствуйте {callback.from_user.username}", reply_markup=get_admin_kb())


@dp.callback_query_handler(text="new_users")
async def date_check_in_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = 'new_users'
    await callback.message.answer(f"Введите промежуток в днях: ")


@dp.callback_query_handler(text="numb_req")
async def date_check_in_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = 'numb_req'
    await callback.message.answer(f"Введите промежуток в днях: ")


@dp.callback_query_handler(text="add_admin")
async def date_check_in_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = 'add_admin'
    await callback.message.answer(f"Введите username: ")


@dp.callback_query_handler(text="start")
async def add_filters_handler(callback: types.CallbackQuery):
    in_proses[callback.from_user.id] = (UserRequest(callback.from_user.id))
    context_dict[callback.from_user.id] = "start"
    await callback.message.answer("Добавьте фильтры или отправьте точку для начала поиска", reply_markup=get_start_kb())


@dp.callback_query_handler(text="radius")
async def add_filters_handler(callback: types.CallbackQuery):
    context_dict[callback.from_user.id] = "radius"
    await callback.message.answer("Выберите радиус: ")


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


@dp.message_handler(content_types=['location'])
async def loc_handler(message):
    print(message.location.longitude, message.location.latitude)
    await message.reply("Начат поиск отелей")
    if in_proses[message.from_user.id] is None:
        await message.answer("Я вас не понимаю")
        return
    in_proses[message.from_user.id].user_point = (message.location.latitude, message.location.longitude)

    hotels = exectr.get_hotels(usr_req=in_proses[message.from_user.id])

    for hotel in hotels:
        await message.answer(hotel)


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

    elif context == "radius":
        in_proses[message.from_user.id].radius_km = int(message.text)
        await message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[message.from_user.id]))

    elif context == "services":
        if in_proses[message.from_user.id].services.count(message.text) == 1:
            in_proses[message.from_user.id].services.remove(message.text)
        elif message.text == "Закончить":
            await message.answer(text="Фильтры добавлены", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Выберите фильтры", reply_markup=get_filter_kb(in_proses[message.from_user.id]))
            context_dict[message.from_user.id] = "add_filters"
        else:
            in_proses[message.from_user.id].services.append(message.text)

    elif context == "new_users":
        users = usr_dao.get_new(int(message.text))
        msg = f"Всего {len(users)} новых пользователей:\n "
        m = min(len(users) - 1, 10)
        for i in range(0, m):
            msg = msg + users[i] + "\n"
        await message.answer(msg, get_back_kb('admin'))

    elif context == "numb_req":
        requests = req_dao.get_new(int(message.text))
        msg = f"Всего было {len(requests)} запросов"
        await message.answer(msg, get_back_kb('admin'))

    elif context == "add_admin":
        usr_dao.set_admin(message.text)
        await message.answer(f"{message.text} добавлены права администратора", get_back_kb('admin'))

    else:
        await message.answer("Я вас не понимаю")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
