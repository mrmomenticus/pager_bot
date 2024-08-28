from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class PlayerMenuButtons:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Когда игра?"),
            KeyboardButton(text="Инвентарь..."),
            KeyboardButton(text="Материалы по игре..."),
            KeyboardButton(text="Список знакомых НПС"),
            KeyboardButton(text="Список заданий"),
            KeyboardButton(text="Нашел ошибку"),
        )
        self.builder = ReplyKeyboardBuilder()
        self.builder.add(*self._buttons)
        self.builder.adjust(*size, True)

    def get_keyboard(self):
        return self.builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Выберите пункт меню...",
        )


class AdminMenuButtons:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить дату игры"),
            KeyboardButton(text="Добавить группу"),
            KeyboardButton(text="Написать игроку"),
            KeyboardButton(text="Пополнить инвентарь..."),
            KeyboardButton(text="Информация по игрокам..."),
            KeyboardButton(text="Инвентарь игрока"),
        )
        self.builder = ReplyKeyboardBuilder()
        self.builder.add(*self._buttons)
        self.builder.adjust(*size, True)

    def get_keyboard(self):
        return self.builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Выберите пункт меню...",
        )


class RegistredButton(ReplyKeyboardBuilder):
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = KeyboardButton(text="Зарегистрироваться")
        self.builder = ReplyKeyboardBuilder()
        self.builder.add(self._buttons)
        self.builder.adjust(*size)

    def get_keyboard(self):
        return self.builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Выберите пункт меню...",
        )



class InformationPlayers(ReplyKeyboardBuilder):
    def __init__ (self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить информацию"),
            KeyboardButton(text="Получить информацию"),
            KeyboardButton(text="Удалить информацию"),
            KeyboardButton(text="Назад"),
        )
        self.builder = ReplyKeyboardBuilder()
        self.builder.add(*self._buttons)
        self.builder.adjust(*size, True)

    def get_keyboard(self):
        return self.builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Выберите пункт меню...",
        )