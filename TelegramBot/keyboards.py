from aiogram import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from Backend.ObjectModels.user import User
from Backend.ObjectModels.user_request import UserRequest

calendar, step = DetailedTelegramCalendar().build()


def get_welcome_kb(user: User):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Начать поиск отелей', callback_data='start'))
    kb.add(types.InlineKeyboardButton(text='Личный кабинет', callback_data='personal_account'))
    if user.is_admin:
        kb.add(types.InlineKeyboardButton(text='Меню администратора', callback_data='admin'))
    return kb


def get_account_opt_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Избранные отели', callback_data='favorites'))
    kb.add(types.InlineKeyboardButton(text='История поиска за 3 дня', callback_data='history'))
    kb.add(types.InlineKeyboardButton(text='Назад', callback_data='welcome'))
    return kb


def get_admin_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Новые пользоватеи', callback_data='new_users'))
    kb.add(types.InlineKeyboardButton(text='Количество запросов', callback_data='numb_req'))
    kb.add(types.InlineKeyboardButton(text='Добавить адимнистратора', callback_data='add_admin'))
    kb.add(types.InlineKeyboardButton(text='Назад', callback_data='welcome'))
    return kb


def get_start_kb():
    start_kb = types.InlineKeyboardMarkup()
    start_kb.add(types.InlineKeyboardButton(text='Добавить фильтры', callback_data='add_filters'))
    return start_kb


def get_filter_kb(usr_req: UserRequest):
    filer_kb = types.InlineKeyboardMarkup(resize_markup=True)
    filer_kb.add(types.InlineKeyboardButton(text='Радиус поиска ' + str(usr_req.radius_km), callback_data='radius'))
    filer_kb.add(types.InlineKeyboardButton(text='Дата заезда: ' + str(usr_req.date_in), callback_data='date_check-in'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Дата выезда: ' + str(usr_req.date_out), callback_data='date_check-out'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Количество взрослых: ' + str(usr_req.adults), callback_data='adults_number'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Возраст детей: ' + list_to_str(usr_req.children_ages),
                                   callback_data='children_ages'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Количество звезд: ' + list_to_str(usr_req.stars),
                                   callback_data='stars_number'))
    filer_kb.add(types.InlineKeyboardButton(text='Цена: ' + usr_req.price, callback_data='price'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Питание: ' + list_to_str(usr_req.meal_types), callback_data='meal_type'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Доп сервисы: ' + list_to_str(usr_req.services), callback_data='services'))
    filer_kb.add(types.InlineKeyboardButton(text='Назад', callback_data='start'))
    print(usr_req)
    return filer_kb


def get_ans_list_kb(ans):
    kb = types.ReplyKeyboardMarkup()
    for el in ans:
        kb.add(types.KeyboardButton(text=el))
    kb.row(types.KeyboardButton(text="Закончить"))
    return kb


def get_back_kb(to):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Назад', callback_data=to))


def get_confirmation_children_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Добавить еще', callback_data='children_ages'))
    kb.add(types.InlineKeyboardButton(text='Закончить', callback_data='add_filters'))
    return kb


def list_to_str(arr):
    st = ""
    for elem in arr:
        st = st + (str(elem) + ", ")
    return st
