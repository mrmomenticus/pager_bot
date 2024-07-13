from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    number_group = State()
    nickname = State()
    