from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
buttons_main_kb = ['Проверить цены.']
main_kb.add(*buttons_main_kb)