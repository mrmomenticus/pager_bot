""" Регистрация пользователей с использованием конечных автоматов. 
    Функции вызывается по очереди и записывает ответ из прошлой. 
"""

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.state.register import RegisterState

import logging
from aiogram import F, Router, types

register_route = Router()

#TODO: Добавить запись в базу данных

@register_route.message(F.text == "Зарегистрироваться")
async def cmd_register_number_group(message: types.Message, state: FSMContext):
    await message.answer(
        "Ну хорошо, скажи мне номер пачки, чтоб я мог определить твоих дружков"
    )

    await state.set_state(RegisterState.number_group)

    logging.debug("Set state: RegisterState.number_group, data: %s", message.text)


@register_route.message(RegisterState.number_group, F.text)
async def cmd_register_nickname(message: types.Message, state: FSMContext):
    await message.answer("Окей, а кликуха у тебя в пачке какая?")

    await state.update_data({"number_group": message.text})
    await state.set_state(RegisterState.nickname)

    logging.debug("Set state: RegisterState.nickname, data: %s", message.text)


@register_route.message(RegisterState.nickname)
async def cmd_register_done(message: types.Message, state: FSMContext):
    await state.update_data({"nickname": message.text})

    data = await state.get_data()

    logging.debug("Set state: RegisterState.done. data: %s", data)

    await message.answer(
        f"Окей, добро пожаловать в мрачный мир будущего " f"{data['nickname']}!"
    )

    await state.clear()
