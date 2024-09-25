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
    
# Блок добавления информации по игрокам
class AddInfoState(StatesGroup):
    name = State()
    photo = State()
    
class GetInfoState(StatesGroup):
    name = State()
    get_info = State()
    
class DeleteInfoState(StatesGroup):
    name = State()
    delete_info = State()

#Инвентарь
class AddMoneyState(StatesGroup):
    name = State()
    money = State()
    
class TakeMoneyState(StatesGroup):
    name = State()
    money = State()
    
class AddItemState(StatesGroup):
    name_player = State()
    name_item = State()
    price_item = State()
    description = State()
    
class DeleteItemState(StatesGroup):
    name_player = State()
    name_item = State()
    delete_item = State()