from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class BaseButtons(ReplyKeyboardBuilder):
    @classmethod
    def _create_builder(self, buttons: tuple, size: list = (1,1)) -> ReplyKeyboardBuilder:
        """
        Создает ReplyKeyboardBuilder на основе переданных кнопок.

        Args:
        buttons (tuple): Кнопки, которые необходимо добавить в ReplyKeyboardBuilder.
        size (list): Размер кнопок в ReplyKeyboardBuilder.

        Returns:
        ReplyKeyboardBuilder: ReplyKeyboardBuilder, который содержит переданные кнопки.
        """
        self._builder = ReplyKeyboardBuilder()
        self._builder.add(*buttons)
        self._builder.adjust(*size)
        self._builder.as_markup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Выберите пункт меню...")
        
        return self._builder

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


class PlayerButtons(BaseButtons):

    def main_menu(self) -> ReplyKeyboardBuilder:
        self.size = (2, 2)
        self._buttons = (
            KeyboardButton(text="Организация"),
            KeyboardButton(text="Инвентарь"),
            KeyboardButton(text="Статы"),
            KeyboardButton(text="Мир игры"),
        )
        return self._create_builder(self._buttons, self.size)
    
    def organization(self) -> ReplyKeyboardBuilder:
        self.size = (1, 2)
        self._buttons = (
            KeyboardButton(text="Когда игра?"),
            KeyboardButton(text="Материалы игры"),
            KeyboardButton(text="Назад"),
        )
        return self._create_builder(self._buttons, self.size)
    
    def inventory(self) -> ReplyKeyboardBuilder:
        self.size = (1, 3)
        self._buttons = (
            KeyboardButton(text="Мои вещи"),
            KeyboardButton(text="Мой кошелек"),
            KeyboardButton(text="Назад"),
        )
        return self._create_builder(self._buttons, self.size)
    
    def stats(self) -> ReplyKeyboardBuilder:
        self.size = (1, 2)
        self._buttons = (
            KeyboardButton(text="Мои статы"),
            KeyboardButton(text="Назад"),
        )
        return self._create_builder(self._buttons, self.size)
    
    def play_world(self) -> ReplyKeyboardBuilder:
        self.size = (1, 5)
        self._buttons = (
            KeyboardButton(text="Квесты"),
            KeyboardButton(text="NPC"),
            KeyboardButton(text="Назад"),
        )
        return self._create_builder(self._buttons, self.size)

class AdminButtons(BaseButtons):
    def main_menu(self) -> ReplyKeyboardBuilder:
        self.size = (1, 3)
        self._buttons = (
            KeyboardButton(text="Организация группы"),
            KeyboardButton(text="Игроки"),
            KeyboardButton(text="Мир игры"),
        )
        return self._create_builder(self._buttons, self.size)
    
    def organization(self) -> ReplyKeyboardBuilder:
        self.size = (1, 1)
        self._buttons = (
            KeyboardButton(text="Добавить дату игры"),
            KeyboardButton(text="Добавить материалы игры"),
            KeyboardButton(text="Список материалов"),
            KeyboardButton(text="Голосование"),
            KeyboardButton(text="Назад"),
        )
        return self._create_builder(self._buttons, self.size)
    
    def players(self) -> ReplyKeyboardBuilder:
        self.size = (1, 1)
        self._buttons = (
            KeyboardButton(text="Добавить вещь"),
            KeyboardButton(text="Удалить вещь"),
            KeyboardButton(text="Добавить денег"),
            KeyboardButton(text="Забрать деньги"),
            KeyboardButton(text="Узнать инвентарь"),
            
            KeyboardButton(text="Назад"),
        )
        return self._create_builder(self._buttons, self.size)
    
    def play_world(self) -> ReplyKeyboardBuilder:
        self.size = (1, 1)
        self._buttons = (
            KeyboardButton(text="Добавить NPC"),
            KeyboardButton(text="Добавить задание"),
            KeyboardButton(text="Список заданий"),
            KeyboardButton(text="Список NPC"),
            KeyboardButton(text="Назад"),
        )
        return self._create_builder(self._buttons, self.size)

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
        