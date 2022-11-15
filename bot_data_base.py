import sqlite3


def create_user_table(connect):
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE NOT NULL, user_name TEXT NOT NULL,)''')
    connect.commit()
    connect.close()


def select_user(connect, user_id: int):
    cursor = connect.cursor()
    cursor.execute(f'''SELECT user_id FROM users WHERE user_id="{user_id}"''')
    what_user = str(connect.fetchone())
    connect.close()
    return what_user == user_id


def add_user_data(user_id: int, user_name: str, connect):
    cursor = connect.cursor()
    cursor.execute(f'''INSERT INTO users (user_id, user_name) VALUES ({user_id, user_name})''')
