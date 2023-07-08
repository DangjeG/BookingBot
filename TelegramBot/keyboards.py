# todo кнопошки для удобного выбора информации
from aiogram import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from Backend.ObjectModels.user_request import UserRequest

calendar, step = DetailedTelegramCalendar().build()

start_searching_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton(text="Отправить координаты", request_location=True))


def get_start_kb():
    start_kb = types.InlineKeyboardMarkup()
    start_kb.add(types.InlineKeyboardButton(text='Добавить фильтры', callback_data='add_filters'))
    start_kb.add(types.InlineKeyboardButton(text='Отправить координаты и начать поиск', callback_data='finish'))
    return start_kb


def get_filter_kb(usr_req: UserRequest):
    filer_kb = types.InlineKeyboardMarkup(resize_markup=True)
    filer_kb.add(types.InlineKeyboardButton(text='Дата заезда: ' + str(usr_req.date_in), callback_data='date_check-in'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Дата выезда: ' + str(usr_req.date_out), callback_data='date_check-out'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Количество взрослых: ' + str(usr_req.adults), callback_data='adults_number'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Возраст детей: ' + list_to_str(usr_req.children_ages),
                                   callback_data='children_ages'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Количество звезд: ' + str(usr_req.stars), callback_data='stars_number'))
    filer_kb.add(types.InlineKeyboardButton(text='Цена: ' + usr_req.price, callback_data='price'))
    filer_kb.add(types.InlineKeyboardButton(text='Питание: ' + usr_req.meal_type, callback_data='meal_type'))
    filer_kb.add(
        types.InlineKeyboardButton(text='Доп сервисы: ' + list_to_str(usr_req.services), callback_data='services'))
    filer_kb.add(types.InlineKeyboardButton(text='Назад', callback_data='start'))
    return filer_kb


def get_meal_type_kb(meal_types):
    kb = types.ReplyKeyboardMarkup()
    for el in meal_types:
        kb.add(types.KeyboardButton(text=el))
    return kb


def get_services_kb(services):
    kb = types.ReplyKeyboardMarkup()
    for el in services:
        kb.add(types.KeyboardButton(text=el))
    kb.row(types.KeyboardButton(text="Закончить"))
    return kb


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
