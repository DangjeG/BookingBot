import datetime


class UserRequest:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_point = (0.0, 0.0)
        self.radius_km = 5
        self.date_in = datetime.date.today()
        self.date_out = datetime.date.today() + datetime.timedelta(days=1)
        self.adults = 1
        self.children_ages = []
        self.stars = 5
        self.meal_type = ""
        self.price = '100-10000'
        self.services = []
