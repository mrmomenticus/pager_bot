
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases import orm
import re

main_menu_admin = Router()

@main_menu_admin.message(F.text == "Добавить время игры")
async def cmd_number_group(message: types.Message, state: FSMContext):
   await message.answer("Введи номер пачки")
   await state.set_state(states.AddDateState.number_group)
    

@main_menu_admin.message(states.AddDateState.number_group, F.text)
async def cmd_register_date(message: types.Message, state: FSMContext):
    await message.answer("Введи дату в формате дд.мм.гггг")

    await state.set_data({"number_group": message.text})
    
    await state.set_state(states.AddDateState.date)

@main_menu_admin.message(states.AddDateState.date, F.text)
async def cmd_add_time(message: types.Message, state: FSMContext):

    pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$')
    if not pattern.match(message.text):
        await message.answer("Неверный формат даты, попробуй ещё раз.")
        return
    
    data = await state.get_data()
    await orm.set_date_game(int(data["number_group"]), message.text)
    await message.answer("Дата успешно добавлена", reply_markup=keyboards.main_menu_admin)
    await state.clear()
    
#TODO: Отделить выше методы в отдельный класс

 

@main_menu_admin.message(F.text == "Добавить группу")
async def cmd_add_group(message: types.Message, state: FSMContext):
    await message.answer("Введи название группы")