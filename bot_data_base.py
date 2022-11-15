import sqlite3


def create_user_table(connect):
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE users
                      (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE NOT NULL, user_name TEXT NOT NULL,)''')
    connect.commit()
    connect.close()


def add_user_data(user_id: int, user_name: str, connect):
    cursor = connect.cursor()
    cursor.execute(f'''INSERT INTO users (user_id, user_name)
                      VALUES ({user_id, user_name})''')
