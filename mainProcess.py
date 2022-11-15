import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply("это стартовое сообщение")

@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply("это комманда help")

@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)

if __name__ == '__main__':
    executor.start_polling(dp)
