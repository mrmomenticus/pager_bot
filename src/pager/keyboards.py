from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class RegistredButton(ReplyKeyboardBuilder):
    def __init__(self, size: list = (2, 2)) -> None:
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


# Класс для вывода основго меню игрока.
class PlayerMenuButtons:
    def __init__(self, size: list = (2, 2)) -> None:
        self._buttons = (
            KeyboardButton(text="Организация..."),
            KeyboardButton(text="Инвентарь и статы..."),
            KeyboardButton(text="Игра..."),
            KeyboardButton(text="Материалы игры"),
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


class PlayerOrganization:
    def __init__(self, size: list = (2, 2)) -> None:
        self._buttons = (
            KeyboardButton(text="Когда игра?"),
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


class PlayerInventory:
    def __init__(self, size: list = (2, 2)) -> None:
        self._buttons = (
            KeyboardButton(text="Мои статы"),
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


class PlayerHelp:
    def __init__(self, size: list = (1, 1)) -> None:
        self._buttons = (
            KeyboardButton(text="Материалы по игре"),
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


class PlayerGame:
    """
    Класс для вывода меню игрока в игре. Вызывается с помощь юкоманды "Игра..."
    """

    def __init__(self, size: list = (2, 2)) -> None:
        self._buttons = (
            KeyboardButton(text="Задания"),
            KeyboardButton(text="NPC"),
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
    def __init__(self, size: list = (1, 1, 1)) -> None:
        self._buttons = (
            KeyboardButton(text="Организация игры..."),
            KeyboardButton(text="Игра..."),
            KeyboardButton(text="Информация по игрокам..."),
            KeyboardButton(text="Инвентарь игрока..."),
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
class AdminHelp:
    def __init__(self, size: list = (1, 1)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить материалы"),
            KeyboardButton(text="Список материалов"),
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

class AdminGame:
    def __init__(self, size: list = (3, 3)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить NPC"),
            KeyboardButton(text="Добавить задание"),
            # KeyboardButton(text="Список заданий"),
            #KeyboardButton(text="Список NPC"),"),
            KeyboardButton(text="Быстрое голосование"),
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


class AdminOrganization:
    def __init__(self, size: list = (1, 1)) -> None:
        self._buttons = (
            KeyboardButton(text="Добавить дату игры"),
            KeyboardButton(text="Добавить группу"),
            KeyboardButton(text="Список игроков группы"),
            # KeyboardButton(text="Написать игроку"),
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


class AdminInformationPlayer(ReplyKeyboardBuilder):
    def __init__(self, size: list = (1, 1)) -> None:
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


class AdminInventoryPlayers(ReplyKeyboardBuilder):
    def __init__(self, size: list = (2, 2)) -> None:
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
        
        

class QuickVote(ReplyKeyboardBuilder):
    def __init__(self, size: list = (2, 2)) -> None:
        self._buttons = (
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет"),
        )
        self.builder = ReplyKeyboardBuilder()
        self.builder.add(*self._buttons)
        self.builder.adjust(*size, True)

    def get_keyboard(self):
        return self.builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
            selective=True,
            input_field_placeholder="Выберите ответ",
        )
        