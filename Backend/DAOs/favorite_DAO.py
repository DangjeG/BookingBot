from database_executor import database_executor
from Backend.ObjectModels.favorite import favorite
from Backend.parsers.parser import Parser


class favorite_DAO:
    def __init__(self):
        self.table_name = "favorites"
        self.executor = database_executor()
        self.executor.create_table(table_name=self.table_name,
                                   columns="user_id INTEGER, hotel_name TEXT, hotel_address TEXT,"
                                           " PRIMARY KEY(user_id, hotel_name, hotel_address),"
                                           " FOREIGN KEY (user_id)  REFERENCES users (user_id),"
                                           " FOREIGN KEY (hotel_name, hotel_address)  REFERENCES hotels (name, address)")

    def add(self, fv: favorite):
        self.executor.insert_data(self.table_name, columns="user_id, hotel_name, hotel_address",
                                  data=f" \"{fv.user_id}\", \"{fv.hotel_name}\", \"{fv.hotel_address}\"")

    def get_by_pk(self, user_id, name, addr):
        temp = \
            self.executor.select_data(table_name=self.table_name,
                                      condition=f"user_id = {user_id} and hotel_name = \"{name}\" and hotel_address = \"{addr}\"")[
                0]
        return self.convert(temp)

    def exist(self, user_id, name, addr):
        return len(
            self.executor.select_data(table_name=self.table_name,
                                      condition=f"user_id = {user_id} and hotel_name = \"{name}\" and hotel_address = \"{addr}\"")) > 0

    def get_user_favorite(self, user_id):
        temps = self.executor.select_data(table_name=self.table_name, condition=f"user_id = {user_id}")
        fvs = []
        for temp in temps:
            fvs.append(self.convert(temp))

    @staticmethod
    def convert(temp):
        return favorite(int(temp[0]), temp[1], temp[2])
