import sqlite3


class database_executor:
    def __init__(self):
        self.conn = sqlite3.connect("../../BookingDB.db")

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        print(query)
        self.conn.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, columns, data):
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({data})"
        self.conn.execute(query)
        self.conn.commit()

    def select_data(self, table_name, columns=None, condition=None):
        if columns:
            query = f"SELECT {columns} FROM {table_name}"
        else:
            query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        try:
            cursor = self.conn.execute(query)
            self.conn.commit()
        except sqlite3.OperationalError:
            return []

        return cursor.fetchall()

    def update_data(self, table_name, set_clause, condition=None):
        query = f"UPDATE {table_name} SET {set_clause}"
        if condition:
            query += f" WHERE {condition}"
        self.conn.execute(query)
        self.conn.commit()

    def delete_data(self, table_name, condition=None):
        query = f"DELETE FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.conn.execute(query)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
