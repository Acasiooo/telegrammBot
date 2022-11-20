from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from datetime import datetime as dt
import datetime

import random

import time

import db as db
from config import TOKEN, TIMEOUT


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


conn = db.create_connection()


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS user(
                                    id        INTEGER  PRIMARY KEY,
                                    user_id   TEXT UNIQUE NOT NULL,
                                    user_name TEXT     NOT NULL,
                                    puk_strong INTEGER  DEFAULT (0) 
                                                        NOT NULL,
                                    last_puk   DATETIME,
                                    puk_count INTEGER DEFAULT (0)
                                );"""

    db_create = db.create_table(conn, sql_create_tasks_table)
    await bot.send_message(message.from_user.id, "/help")


@dp.message_handler(commands=["add_me"])
async def process_addme_command(message: types.Message):
    user_data = [
        str(message.from_user.id),
        str(message.from_user.first_name)
    ]
    sql_create_tasks_add_user = ('''INSERT INTO user (
                                        user_id, user_name) values 
                                        (?, ?);''')

    await bot.send_message(message.from_user.id, str(db.add_user_data(conn, sql_create_tasks_add_user, user_data)))


@dp.message_handler(commands=["help"])
async def help(message: types.Message):

    await bot.send_message(message.from_user.id,    '/start      - началть работать с ботом\n'
                                                    '/add_me     - зарегистрироваться играть\n'
                                                    '/puk        - пукнуть\n'
                                                    '/top        - посмотреть таблицу рекордов\n'
                                                    '/statistics - просмотр статуса\n'
                                                    '/help       - помощь')


@dp.message_handler(commands=["top"])
async def top_user(message: types.Message):
    sql_create_tasks_select_user_id = ('''SELECT
	                                                user_name,
	                                                puk_strong
                                          FROM
	                                                user
                                          ORDER BY
	                                                puk_strong DESC
                                          LIMIT 10;''')

    top_users = ''

    search_user = db.select_from(conn, sql_create_tasks_select_user_id)
    for i in search_user:
        top_users += '{0:15}  {1}\n'.format(i[0], i[1])

    if search_user:
        await bot.send_message(message.from_user.id, f"< ---TOP_USERS--- >\n{top_users}")


@dp.message_handler(commands=["statistics"])
async def statistics(message: types.Message):
    sql_create_tasks_user_stats = '''SELECT user_name, puk_strong, puk_count, last_puk FROM user WHERE user_id = (?)'''
    user_stats = db.select_from(conn, sql_create_tasks_user_stats, message.from_user.id)[0]

    stat = (f'имя - {user_stats[0]}\n'
            f'сила пука - {user_stats[1]}\n'
            f'колличество пуков - {user_stats[2]}\n'
            f'последний пук - {user_stats[3]}')

    await bot.send_message(message.from_user.id, stat)



@dp.message_handler(commands=["all_users"])
async def all_users(message: types.Message):
    sql_create_tasks_select_user_id = ('''SELECT * FROM user;''')

    search_user = db.select_from(conn, sql_create_tasks_select_user_id)
    if search_user:
        await bot.send_message(message.from_user.id, str(search_user))


@dp.message_handler(commands=["puk"])
async def add_puk(message: types.Message):
    sql_create_tasks_test_user_in_db = ('''SELECT * FROM user WHERE (?)''')
    user_data = db.test_user_and_data(
        conn, sql_create_tasks_test_user_in_db, message.from_user.id)[0]

    if user_data[4] == None:
        sql_create_tasks_set_last_puk = ('''UPDATE user SET 
                                        last_puk = (?)
                                        WHERE user_id = (?);''')
        db.set_datetime(conn, sql_create_tasks_set_last_puk, message.from_user.id, str(dt.now() - datetime.timedelta(minutes=2))[0:19])
        user_data = db.test_user_and_data(
        conn, sql_create_tasks_test_user_in_db, message.from_user.id)[0]
    if user_data[4] != None and (dt.strptime(user_data[4], "%Y-%m-%d %H:%M:%S")) < (dt.now() - datetime.timedelta(minutes=2)):

        puk_text = ""

        puk_rd = random.randint(-10, 10)

        if puk_rd > 0:
            puk_text = f"Ваша скорость пука увеличелась на {puk_rd}м/с \nтеперь она составляет: "
        elif puk_rd < 0:
            puk_text = f"Ваша скорость пука понизилась на {puk_rd}м/с \nтеперь она составляет: "
        else:
            puk_text = f"Ваша скорость пука не изменилась {puk_rd}м/с \nона составляет: "

        sql_create_tasks_get_puk = (
            '''SELECT puk_strong FROM user WHERE user_id = (?)''')
        
        sql_create_tasks_update_last_puk = ('''UPDATE user SET 
                                        last_puk = (?), puk_strong = (?), puk_count = puk_count + 1
                                        WHERE user_id = (?);''')
        

        if db.set_datetime_and_puk(conn, sql_create_tasks_update_last_puk, message.from_user.id, str(dt.now())[0:19], puk_rd+db.select_from(
            conn, sql_create_tasks_get_puk, message.from_user.id)[0][0]) == True:

            await bot.send_message(message.from_user.id, str(puk_text + str(db.select_from(
            conn, sql_create_tasks_get_puk, message.from_user.id)[0][0]))+"м/с")
        else:
            await bot.send_message(message.from_user.id, "произошла ошибка")

    else:
        timeout = dt.strptime(
            user_data[4], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=2) - dt.now()
        await bot.send_message(message.from_user.id, f'на сегодня вы исчерпали все попытки можете попытаться ещё через: {str(timeout)[:-7]}')
        print(str(timeout))


@dp.message_handler(commands=["test"])
async def select_from(message: types.Message):

    sql_create_tasks_select_user_id = (
        '''SELECT user_name FROM user WHERE (?)''')

    search_user = db.select_from(
        conn, sql_create_tasks_select_user_id, message.from_user.id)
    if search_user:
        await bot.send_message(message.from_user.id, str(search_user))


if __name__ == '__main__':
    executor.start_polling(dp)
