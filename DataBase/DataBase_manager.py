import sqlite3
import time


class DataBase:
    def __init__(self, file='data_base/users_tg_bot.db'):  # TODO
        self.__connection = sqlite3.connect(file, check_same_thread=False)
        self.__cursor = self.__connection.cursor()

    def create_table_users(self):
        query_create = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            language_code TEXT
        )
        '''
        self.__cursor.execute(query_create)
        self.__connection.commit()

    def create_table_messages(self):
        query_create = '''
            CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                date INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id) 
        )
        '''
        self.__cursor.execute(query_create)
        self.__connection.commit()

    def create_table_cities(self):
        query_create = '''
            CREATE TABLE IF NOT EXISTS cities(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                city TEXT
                FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        '''
        self.__cursor.execute(query_create)
        self.__connection.commit()

    def save_user(self, user):
        query_create = '''
            INSERT OR IGNORE INTO users (user_id, first_name, last_name, username, language_code)
            VALUES (?, ?, ?, ?, ?)
            '''
        self.__cursor.execute(query_create,
                              (user.id, user.first_name, user.last_name, user.username, user.language_code))
        self.__connection.commit()

    def save_message(self, user_id, message_id, text, date):
        query_create = '''
            INSERT INTO messages (user_id, message_id, text, date)
            VALUES (?, ?, ?, ?)
            '''
        self.__cursor.execute(query_create, (user_id, message_id, text, date))
        self.__connection.commit()

    def save_city(self, user_id, new_city):
        query_create = '''
            UPDATE cities SET city = ?
            WHERE user_id = ?
            '''
        self.__cursor.execute(query_create, (new_city, user_id))
        self.__connection.commit()

    def __del__(self):
        print("Объект DataBase был уничтожен")
        self.__connection.close()

    def get_city(self, user_id):
        query_create = '''
                    SELECT city FROM cities
                    WHERE user_id = ?
                    '''
        self.__cursor.execute(query_create,
                              (user_id, ))
        return self.__cursor.fetchall()
