import datetime


class User:
    def __init__(self, user_id, username, registration_date=datetime.date.today(), is_admin=False):
        self.user_id = user_id
        self.username = username
        self.registration_date = registration_date
        self.is_admin = is_admin
