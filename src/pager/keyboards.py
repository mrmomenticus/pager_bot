from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class PlayerMenuButtons(ReplyKeyboardBuilder):
    def __init__(self, size: list = (3, 3, 3, 3)) -> None:
        self.buttons = (
            "Когда игра?",
            "Инвентарь...",
            "Материалы по игре...",
            "Список знакомых НПС",
            "Список заданий",
            "Нашел ошибку",
        )
        self.add(*self.buttons)
        self.adjust(*size)
        self.as_markup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder = "Выберите пункт меню...")

    def get_markup(self):
        return self
        
    

class AdminMenuButtons(ReplyKeyboardBuilder):
    def __init__(self, size: list = (3, 3, 3, 3)) -> None:
        self._buttons = (
            "Добавить дату игры",
            "Добавить новую группу",
            "Написать игроку",
            "Пополнить инвентарь...",
            "Информация по игрокам...",
            "Инвентарь игрока", 
        )
        self.add(self._buttons)
        self.adjust(*size)
        self.as_markup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder = "Выберите пункт меню...")
        
    def get_markup(self):
        return self
    
    
class RegistredButton(ReplyKeyboardBuilder):
    def __init__(self, size: list = (3, 3, 3, 3)) -> None:
        self._buttons = (
            "Зарегистрироваться",
        )
        self.add(self._buttons)
        self.adjust(*size)
        self.as_markup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder = "Выберите пункт меню...")

    def get_markup(self):
        return self