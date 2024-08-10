from aiogram.fsm.context import FSMContext
from pager import states

import logging
from aiogram import F, Router, types


register_route = Router()


@register_route.message(F.text == "Зарегистрироваться")
async def cmd_register_number_group(message: types.Message, state: FSMContext):
    await message.answer(
        "<b>Ну хорошо, скажи мне номер пачки, чтоб я мог определить твоих дружков</b>",
        parse_mode="html",
    )
    await state.set_state(states.RegisterState.number_group)
    logging.debug("Set state: RegisterState.number_group")


async def cmd_register_nickname(message: types.Message, state: FSMContext):
    await message.answer(
        "<b>Окей, а кликуха у тебя в пачке какая?</b>", parse_mode="html"
    )
    await state.set_state(states.RegisterState.nickname)
    logging.debug("Set state: RegisterState.nickname")
