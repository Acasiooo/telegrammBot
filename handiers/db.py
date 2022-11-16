import sqlite3
from sqlite3 import Error


def create_connection():
    conn = None;
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
        return "база была успешно создана"
    except Error as e:
        print(e)
        return "Ошибка база данных уже была создана"



def select_user(conn, sql_create_tasks_select_user_id, user_id):
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_select_user_id, [user_id])
        return c.fetchall()
    except Error as e:
        print(e)
        return e


def all_users(conn, sql_create_tasks_select_user_id):
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_select_user_id)
        return c.fetchall()
    except Error as e:
        print(e)
        return e


def add_user_data(conn, create_tasks_add_user, user_data):
    try:
        c = conn.cursor()
        c.execute(create_tasks_add_user, user_data)
        conn.commit()
        return "user added"
    except Error as e:
        print(e)
        return e


if __name__ == '__main__':
    create_connection()
