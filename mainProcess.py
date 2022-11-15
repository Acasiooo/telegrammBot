import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import bot_data_base
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


connect = sqlite3.connect("bot_user_DB.db")


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply("это стартовое сообщение")
    await bot_data_base.create_user_table(connect)

@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply("это комманда help")
    await bot_data_base.add_user_data(message.from_user.id, message.from_user.first_name, connect)

@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, str(message.from_user.first_name))


@dp.message_handler(commands=["test"])
async def select_user(message: types.Message):
    if bot_data_base.select_user():
        await bot.send_message(message.from_user.id, str(message.from_user.first_name))


if __name__ == '__main__':
    executor.start_polling(dp)
