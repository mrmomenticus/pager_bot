import logging
from aiogram import types
from aiogram.fsm.context import FSMContext
async def handler_error(error: Exception, message: types.Message, state: FSMContext = None, *args):
    await message.answer("Возникла ошибка. Попробуйте позже")
    logging.critical(error, args)
    await state.clear()

class NotFoundError(Exception):
    """
    Ошибка поиска данных. Например: группа была не найдена в БД

    Args:
        *args: список подаваемых данных при запроса
    """

    def __init__(self, *args):
        self.args = args
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Таких данных не найдено: {', '.join(map(str, self.args))}"

    
class AlreadyAvailableError(Exception):
    def __str__(self):
        return "Такое уже есть!"