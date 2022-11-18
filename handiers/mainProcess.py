from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import db as db
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


conn = db.create_connection()

''''''
@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    sql_create_tasks_table = """CREATE TABLE if not exists users(
                                        id integer PRIMARY KEY,
                                        user_id text NOT NULL,
                                        user_name text NOT NULL
                                    );"""
    await bot.send_message(message.from_user.id, str(db.create_table(conn, sql_create_tasks_table)))

@dp.message_handler(commands=["addme"])
async def process_addme_command(message: types.Message):
    user_data = [
    str(message.from_user.id),
    str(message.from_user.first_name)
    ]
    sql_create_tasks_add_user = ('''INSERT INTO users (
                                        user_id, user_name) values 
                                        (?, ?);''')

    await bot.send_message(message.from_user.id, str(db.add_user_data(conn, sql_create_tasks_add_user, user_data)))


@dp.message_handler(commands=["all_users"])
async def all_users(message: types.Message):
    sql_create_tasks_select_user_id = ('''SELECT * FROM users;''')

    search_user = db.all_users(conn, sql_create_tasks_select_user_id)
    if search_user:
        await bot.send_message(message.from_user.id, str(search_user))


@dp.message_handler(commands=["test"])
async def select_user(message: types.Message):

    sql_create_tasks_select_user_id = ('''SELECT user_name FROM users WHERE (?)''')

    search_user = db.select_user(conn, sql_create_tasks_select_user_id, message.from_user.id)
    if search_user:
        await bot.send_message(message.from_user.id, str(search_user))


if __name__ == '__main__':
    executor.start_polling(dp)
