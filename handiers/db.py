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
        c.close()
        print("база была успешно создана")
        return '''/start   - началть работать с ботом\n
/add_me  - начать играть\n
/puk     - пукнуть\n
/top     - посмотреть таблицу рекордов\n
/view_me - просмотр мощьности пердежа\n
/help    - помощь'''
    except Error as e:
        print(e)
        return "Ошибка база данных уже была создана"



def select_user(conn, sql_create_tasks_select_user_id, user_id):
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_select_user_id, [user_id])
        data = c.fetchall()
        c.close()
        return data
    except Error as e:
        print(e)
        return e


def test_user_and_data(conn, sql_create_tasks_select_user_id, user_id):
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_select_user_id, [user_id])
        data = c.fetchall()
        c.close()
        return data
    except Error as e:
        print(e)
        return False


def all_users(conn, sql_create_tasks_select_user_id):
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_select_user_id)
        data = c.fetchall()
        c.close()
        return data
    except Error as e:
        print(e)
        return e


def add_user_data(conn, create_tasks_add_user, user_data):
    try:
        c = conn.cursor()
        c.execute(create_tasks_add_user, user_data)
        conn.commit()
        c.close()
        return "user added"
    except Error as e:
        print(e)
        return "Вы уже зарегестрированны в боте"


def set_datetime(conn, create_tasks_add_data, user_data, time):
    try:
        c = conn.cursor()
        c.execute(create_tasks_add_data, [time, user_data])
        conn.commit()
        c.close()
        return "data commit"
    except Error as e:
        print(e)
        return e


def set_datetime_and_puk(conn, create_tasks_add_data, user_data, time, puk):
    try:
        c = conn.cursor()
        c.execute(create_tasks_add_data, [time, puk, user_data])
        conn.commit()
        c.close()
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
