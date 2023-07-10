import datetime


class UserRequest:
    def __init__(self, user_id, creation_date=datetime.date.today()):
        self.user_id = user_id
        self.user_point = (55.160797, 61.402509)
        self.radius_km = 5
        self.date_in = datetime.date.today()
        self.date_out = datetime.date.today() + datetime.timedelta(days=1)
        self.adults = 1
        self.children_ages = []
        self.stars = []
        self.meal_types = []
        self.price = '100-100000'
        self.services = []
        self.creation_date = creation_date

    def __str__(self):
        return f"Геопозиция: {self.user_point}, \n" \
               f"Радиус поиска: {self.radius_km}, \n" \
               f"Дата заезда: {self.date_in}, \n" \
               f"Дата выезда: {self.date_out}, \n" \
               f"Количество взрослых: {self.adults}, \n" \
               f"Возраст детей: {list_to_str(self.children_ages)}, \n" \
               f"Количество звезд: {list_to_str(self.stars)}, \n" \
               f"Тип питания: {list_to_str(self.meal_types)}, \n" \
               f"Цена: {self.price}, \n" \
               f"Доп сервисы: {list_to_str(self.services)})"


def list_to_str(arr):
    st = ""
    for elem in arr:
        st = st + (str(elem) + ", ")
    return st
