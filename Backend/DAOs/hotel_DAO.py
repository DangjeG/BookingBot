from database_executor import database_executor


class hotel_DAO:
    def __init__(self):
        self.table_name = "hotels"
        self.executor = database_executor()

    def add(self):
        self.executor.create_table(table_name=self.table_name, columns="name VARCHAR, address VARCHAR,"
                                                                       " rating VARCHAR, url VARCHAR, photo_url VARCHAR, date_of_saving date")
        self.executor.insert_data()
