import psycopg2

# Установка параметров подключения
connection_params = {
    "host": "your_host",
    "port": "your_port",
    "database": "your_database",
    "user": "your_username",
    "password": "your_password"
}

# Установка соединения
conn = psycopg2.connect(**connection_params)

# Создание курсора
cursor = conn.cursor()

# Выполнение SQL-запросов
cursor.execute("SELECT * FROM your_table")
result = cursor.fetchall()

# Обработка результатов запроса
for row in result:
    print(row)

# Закрытие курсора и соединения
cursor.close()
conn.close()
