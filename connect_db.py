import sqlite3
import logging

# подключение к БД
async def db_connection():
    global connection, cursor
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    logging.info('Подключение к БД произошло успешно')

    # если таблицы users не существует, создать её
    cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, user_name TEXT)')
    connection.commit()
    logging.info('Создана таблица users')

# запись нового пользователя
async def new_user(user_id, user_name):
    user = cursor.execute('SELECT 1 FROM users WHERE user_id == "{key}"'.format(key=user_id)).fetchone()

    # если пользователя не существует в БД
    if not user:
        # осуществляется запись в БД
        cursor.execute('INSERT INTO users VALUES (?, ?)', (user_id, user_name))
        connection.commit()
        logging.info(f'Пользователь {user_name} успешно внесён в БД')

# если таблицы requests не существует, создать её
async def table_requests():
    cursor.execute('CREATE TABLE IF NOT EXISTS requests(first_param VARCHAR, second_param VARCHAR, third_param VARCHAR, result TEXT)')
    connection.commit()
    logging.info('Создана таблица requests')

# запись конвертации в БД
async def record_result(first_param, second_param, third_param, result):
    cursor.execute('INSERT INTO requests VALUES (?, ?, ?, ?)', (first_param, second_param, third_param, result))
    connection.commit()
    logging.info('Результат внесён в БД')