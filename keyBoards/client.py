from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton("/")
b2 = KeyboardButton("/")
b3 = KeyboardButton("/")

kb_client = ReplyKeyboardMarkup()

kb_client.add(b1).add(b2).add(b3)