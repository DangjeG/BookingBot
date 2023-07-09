import sqlite3

class DataBaseHelper:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def create_table(self, tablename, columns):
        query = f"CREATE TABLE IF NOT EXISTS {tablename} ({columns})"
        self.conn.execute(query)

    def insert_data(self, tablename, data):
        query = f"INSERT INTO {tablename} VALUES ({data})"
        self.conn.execute(query)

    def select_data(self, tablename, columns=None, condition=None):
        if columns:
            query = f"SELECT {columns} FROM {tablename}"
        else:
            query = f"SELECT * FROM {tablename}"
        if condition:
            query += f" WHERE {condition}"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def update_data(self, tablename, set_clause, condition=None):
        query = f"UPDATE {tablename} SET {set_clause}"
        if condition:
            query += f" WHERE {condition}"
        self.conn.execute(query)

    def delete_data(self, tablename, condition=None):
        query = f"DELETE FROM {tablename}"
        if condition:
            query += f" WHERE {condition}"
        self.conn.execute(query)

    def close_connection(self):
        self.conn.close()