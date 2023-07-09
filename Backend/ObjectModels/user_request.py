import datetime


class UserRequest:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_point = (55.160797, 61.402509)
        self.radius_km = 5
        self.date_in = datetime.date.today()
        self.date_out = datetime.date.today() + datetime.timedelta(days=1)
        self.adults = 1
        self.children_ages = []
        self.stars = 5
        self.meal_types = ""
        self.price = '100-10000'
        self.services = []

    def __str__(self):
        return f"UserRequest(user_id={self.user_id}, " \
               f"user_point={self.user_point}, " \
               f"radius_km={self.radius_km}, " \
               f"date_in={self.date_in}, " \
               f"date_out={self.date_out}, " \
               f"adults={self.adults}, " \
               f"children_ages={self.children_ages}, " \
               f"stars={self.stars}, " \
               f"meal_types={self.meal_types}, " \
               f"price={self.price}, " \
               f"services={self.services})"

