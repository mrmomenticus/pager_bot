from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


registred_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Зарегистрироваться")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...",
)

main_menu_players = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Когда игра?"),
            KeyboardButton(text="Инвентарь"),
            KeyboardButton(text="Связь с ГМ"),
            KeyboardButton(text="Нашел ошибку"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...",
)

main_menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить время игры"),
            KeyboardButton(text="Написать игроку"),
            KeyboardButton(text="Дать денег"),
            KeyboardButton(text="Добавить группу")
        ]
    ]
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...",
)
