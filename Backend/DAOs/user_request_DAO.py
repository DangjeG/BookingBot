import datetime

from Backend.DAOs.database_executor import database_executor
from Backend.ObjectModels.user_request import UserRequest


class user_request_DAO:
    def __init__(self):
        self.table_name = "user_requests"
        self.executor = database_executor()
        self.executor.create_table(table_name=self.table_name, columns="user_id INTEGER,"
                                                                       " user_point TEXT,"
                                                                       " radius_km INTEGER,"
                                                                       " date_in TEXT,"
                                                                       " date_out TEXT,"
                                                                       " adults INTEGER,"
                                                                       " children_ages TEXT,"
                                                                       " stars TEXT,"
                                                                       " meal_types TEXT,"
                                                                       " price TEXT,"
                                                                       " services TEXT,"
                                                                       " creation_date TEXT,"
                                                                       " FOREIGN KEY (user_id)  REFERENCES users (user_id)"
                                   )

    def add(self, ur: UserRequest):
        self.executor.insert_data(self.table_name, columns="user_id, user_point, radius_km, date_in, "
                                                           "date_out, adults, children_ages, stars,"
                                                           " meal_types, price, services, creation_date",
                                  data=f" {ur.user_id}, \"{self.tuple_to_string(ur.user_point)}\", \"{ur.radius_km}\", \"{ur.date_in}\","
                                       f" \"{ur.date_out}\", \"{ur.adults}\", \"{self.list_to_string(ur.children_ages)}\", \"{self.list_to_string(ur.stars)}\","
                                       f" \"{self.list_to_string(ur.meal_types)}\", \"{ur.price}\", \"{self.list_to_string(ur.services)}\", \"{ur.creation_date}\"")

    def get_by_user_id(self, user_id):
        temps = self.executor.select_data(table_name=self.table_name,
                                          condition=f"user_id = \"{user_id}\"")
        res = []
        for temp in temps:
            res.append(self.convert(temp))
        return res

    def get_new(self, days):
        temps = self.executor.select_data(table_name=self.table_name,
                                          condition=f"creation_date > \'{datetime.date.today() - datetime.timedelta(days=days)}\'")
        reqs = []
        for temp in temps:
            reqs.append(self.convert(temp))
        return reqs

    def delete_old(self, days):
        self.executor.delete_data(table_name=self.table_name,
                                  condition=f"creation_date < \'{datetime.date.today() - datetime.timedelta(days=days)}\'")

    @staticmethod
    def convert(temp):
        req = UserRequest(temp[0])
        req.user_point = user_request_DAO.string_to_tuple(temp[1])
        req.radius_km = int(temp[2])
        req.date_in = datetime.datetime.strptime(temp[3], "%Y-%m-%d").date()
        req.date_out = datetime.datetime.strptime(temp[4], "%Y-%m-%d").date()
        req.adults = int(temp[5])
        req.children_ages = user_request_DAO.string_to_list(temp[6], True)
        req.stars = user_request_DAO.string_to_list(temp[7], True)
        req.meal_types = user_request_DAO.string_to_list(temp[8])
        req.price = temp[9]
        req.services = user_request_DAO.string_to_list(temp[10])
        req.creation_date = datetime.datetime.strptime(temp[11], "%Y-%m-%d").date()

        return req

    @staticmethod
    def string_to_list(st, to_int=False):
        arr = str.split(st, ", ")
        res = []
        for elem in arr:
            if elem == "":
                continue
            if to_int:
                res.append(int(elem))
            else:
                res.append(elem)
        return res

    @staticmethod
    def list_to_string(lis):
        st = ""
        for elem in lis:
            st = st + (str(elem) + ", ")
        return st

    @staticmethod
    def tuple_to_string(tpl):
        return f"{tpl[0]};{tpl[1]}"

    @staticmethod
    def string_to_tuple(st):
        arr = str.split(st, ";")
        return float(arr[0]), float(arr[1])

