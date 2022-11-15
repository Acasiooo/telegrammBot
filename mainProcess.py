import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import bot_data_base
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


conn = bot_data_base.create_connection()


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply("создание таблицы")
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        user_id text NOT NULL,
                                        user_name text NOT NULL
                                    );"""
    bot_data_base.create_table(conn, sql_create_tasks_table)

@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply("это комманда help")
    bot_data_base.add_user_data(message.from_user.id, message.from_user.first_name)

@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, str(message.from_user.first_name))


@dp.message_handler(commands=["test"])
async def select_user(message: types.Message):
    if bot_data_base.select_user(message.from_user.id):
        await bot.send_message(message.from_user.id, str(message.from_user.first_name))


if __name__ == '__main__':
    executor.start_polling(dp)
