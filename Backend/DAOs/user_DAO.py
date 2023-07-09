import datetime

from database_executor import database_executor
from Backend.ObjectModels.user import User


class user_DAO:
    def __init__(self):
        self.table_name = "users"
        self.executor = database_executor()
        self.executor.create_table(table_name=self.table_name, columns="user_id INTEGER PRIMARY KEY, username TEXT,"
                                                                       " registration_date TEXT, is_admin TEXT")

    def add(self, usr: User):
        self.executor.insert_data(self.table_name, columns="user_id, username, registration_date, is_admin",
                                  data=f" {usr.user_id}, \"{usr.username}\", \"{usr.registration_date}\", \"{usr.is_admin}\"")

    def get_by_pk(self, user_id):
        temp = self.executor.select_data(table_name=self.table_name,
                                         condition=f"user_id = \"{user_id}\"")[0]
        return self.convert(temp)

    def exist(self, user_id):
        return len(
            self.executor.select_data(table_name=self.table_name,
                                      condition=f"user_id = {user_id}")) > 0

    @staticmethod
    def convert(temp):
        return User(temp[0], temp[1], datetime.datetime.strptime(temp[2], "%Y-%m-%d").date(), bool(temp[3]))

    def get_new(self, days):
        temps = self.executor.select_data(table_name=self.table_name, condition=f"registration_date > \'{datetime.date.today() - datetime.timedelta(days=days)}\'")
        users = []
        for temp in temps:
            users.append(self.convert(temp))
        return users

    def set_admin(self, username):
        self.executor.update_data(table_name=self.table_name, set_clause=f"is_admin = \"True\"",
                                  condition=f"username = \"{username}\"")



