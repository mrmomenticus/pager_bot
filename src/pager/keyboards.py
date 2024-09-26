from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Класс для вывода основго меню игрока.
class PlayerMenuButtons:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Организация игры..."),
            KeyboardButton(text="Инвентарь..."),
            KeyboardButton(text="Игра..."),
            KeyboardButton(text="Справка..."),
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


class InventoryForPlayer:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Мои вещи"),
            KeyboardButton(text="Мои деньги"),
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


class HelpPlayers:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Мой персонаж"),
            KeyboardButton(text="Хронология игры"),
            # KeyboardButton(text="Карта мира"),
            # KeyboardButton(text="Правила игры"),
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


class GamePlayers:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Задания"),
            KeyboardButton(text="НПС"),
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


class AdminMenuButtons:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить дату игры"),
            KeyboardButton(text="Добавить группу"),
            KeyboardButton(text="Написать игроку"),
            KeyboardButton(text="Хронология игры..."),
            KeyboardButton(text="Информация по игрокам..."),
            KeyboardButton(text="Инвентарь игрока..."),
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


class OrganizationGame:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить дату игры"),
            KeyboardButton(text="Добавить группу"),
            KeyboardButton(text="Написать игроку"),
            KeyboardButton(text="Добавить задание..."),
            KeyboardButton(text="Добавить НПС..."),
            KeyboardButton(text="Инвентарь игрока..."),
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
    def __init__(self, size: list = (3, 3)) -> None:
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


class InventoryPlayersForAdmin(ReplyKeyboardBuilder):
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить вещь"),
            KeyboardButton(text="Добавить денег"),
            KeyboardButton(text="Узнать инвентарь игрока"),
            KeyboardButton(text="Удалить вещь"),
            KeyboardButton(text="Забрать деньги"),
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
