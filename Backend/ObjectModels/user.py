import datetime


class User:
    def __init__(self, user_id, username, favorites, registration_date=None):
        self.user_id = user_id
        self.username = username
        if registration_date:
            self.registration_date = registration_date
        else:
            self.registration_date = datetime.date.today()
        self.favorites = favorites
