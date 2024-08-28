from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    is_admin = State()
    number_group = State()
    nickname = State()

class AddDateState(StatesGroup):
    number_group = State()
    date = State()
    
class AddGroupState(StatesGroup):
    number_group = State()
    group_name = State()
    
class AddInfoState(StatesGroup):
    name = State()
    photo = State()
    
class GetInfoState(StatesGroup):
    name = State()
    get_info = State()
    
class DeleteInfoState(StatesGroup):
    name = State()
    delete_info = State()