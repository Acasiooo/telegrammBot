import sqlite3
from sqlite3 import Error


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('botSQL.db')
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        return True
    except Error as e:
        print(e)
        return False


def add_user_data(conn, create_tasks_add_user, user_data):
    try:
        c = conn.cursor()
        c.execute(create_tasks_add_user, user_data)
        conn.commit()
        return "user added"
    except Error as e:
        print(e)
        return "Вы уже зарегестрированны в боте"


def select_from(conn, sql_create_tasks_select_user_id, user_id = None):
    try:
        c = conn.cursor()
        if user_id !=None:
            c.execute(sql_create_tasks_select_user_id, [user_id])
            data = c.fetchall()
            return data
        else:
            c.execute(sql_create_tasks_select_user_id)
            data = c.fetchall()
            return data
    except Error as e:
        print(e)
        return e


def test_user_and_data(conn, sql_create_tasks_select_user_id, user_id):
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_select_user_id, [user_id])
        data = c.fetchall()
        return data
    except Error as e:
        print(e)
        return False


def set_datetime(conn, create_tasks_add_data, user_data, time):
    try:
        c = conn.cursor()
        c.execute(create_tasks_add_data, [time, user_data])
        conn.commit()
        return "data commit"
    except Error as e:
        print(e)
        return e


def set_datetime_and_puk(conn, create_tasks_add_data, user_data, time, puk):
    try:
        c = conn.cursor()
        c.execute(create_tasks_add_data, [time, puk, user_data])
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def get_puk(conn, sql_create_tasks_select_user_id, user_id):
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_select_user_id, [user_id])
        return c.fetchall()[0][0]
    except Error as e:
        print(e)
        return e


def bd_parsing(query):
    for i in query:
        for f in i:
            print(f)


if __name__ == '__main__':
    create_connection()
