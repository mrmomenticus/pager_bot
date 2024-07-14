from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


registred_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Зарегистрироваться')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

