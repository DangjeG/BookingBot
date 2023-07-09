from database_executor import database_executor
from Backend.ObjectModels.hotel import Hotel


class hotel_DAO:
    def __init__(self):
        self.table_name = "hotels"
        self.executor = database_executor()
        self.executor.create_table(table_name=self.table_name, columns="name TEXT, address TEXT,"
                                                                       " rating TEXT, url TEXT, photo_url TEXT, PRIMARY KEY(name, address)")

    def add(self, htl: Hotel):
        self.executor.insert_data(self.table_name, columns="name, address, rating, url, photo_url",
                                  data=f" \"{htl.name}\", \"{htl.address}\", \"{htl.rating}\", \"{htl.url}\", \"{htl.photo_url}\"")

    def get_by_pk(self, name, addr):
        temp = \
        self.executor.select_data(table_name=self.table_name, condition=f"name = \"{name}\" and address = \"{addr}\"")[
            0]
        return self.convert(temp)

    def exist(self, name, addr):
        return len(
            self.executor.select_data(table_name=self.table_name, condition=f"name = {name} and address = {addr}")) > 0

    @staticmethod
    def convert(temp):
        return Hotel(temp[0], temp[1], temp[2], temp[3], temp[4])
