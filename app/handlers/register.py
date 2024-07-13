from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.state.register import RegisterState

import logging
from aiogram import  F, Router, types
from aiogram.filters.command import CommandStart, Command


register_route = Router()

# async def start_register(message: Message, state: FSMContext):
#     await message.answer("Ну как тебя зовут?")
#     await state.set_state(RegisterState.name)
    
@register_route.message(F.text == "Зарегистрироваться")
async def cmd_register_number_group(message: types.Message, state: FSMContext):
    await message.answer("<b>Ну хорошо, скажи мне номер пачки, чтоб я мог определить твоих дружков</b>", parse_mode="html")
    await state.set_state(RegisterState.number_group)
    logging.debug("Set state: RegisterState.number_group")
    

async def cmd_register_nickname(message: types.Message, state: FSMContext):
    await message.answer("<b>Окей, а кликуха у тебя в пачке какая?</b>", parse_mode="html")
    await state.set_state(RegisterState.nickname)
    logging.debug("Set state: RegisterState.nickname")