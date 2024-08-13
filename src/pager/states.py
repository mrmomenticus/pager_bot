from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    is_admin = State()
    number_group = State()
    nickname = State()

