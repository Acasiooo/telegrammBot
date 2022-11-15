import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:
        conn = sqlite3.connect('botSQL.db')
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def select_user(user_id: int):
    cursor = config.CONNECT
    cursor.execute(f'''SELECT user_id FROM users WHERE user_id="{user_id}"''')
    what_user = str(cursor.fetchone())
    return what_user == user_id


def add_user_data(user_id: int, user_name: str):
    user = (0, user_id, user_name)

    cursor = config.CONNECT
    cursor.execute('''insert into users values (?, ?, ?)''', user)
    cursor.commit()


if __name__ == '__main__':
    create_connection()
