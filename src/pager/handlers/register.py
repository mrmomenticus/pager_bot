"""Регистрация пользователей с использованием конечных автоматов.
Функции вызывается по очереди и записывает ответ из прошлой.
"""

from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases import orm, core
import logging
from aiogram import F, Router, types

register_route = Router()

new_player = core.Player()


@register_route.message(F.text == "Зарегистрироваться")
async def cmd_register_number_group(message: types.Message, state: FSMContext):
    new_player.id_tg = message.from_user.id
    new_player.username = message.from_user.username
    await message.answer(
        "Ну хорошо, скажи мне номер пачки, чтоб я мог определить твоих дружков"
    )

    await state.set_state(states.RegisterState.number_group)

    logging.debug(
        "Set state: states.RegisterState.number_group, data: %s", message.text
    )


@register_route.message(states.RegisterState.number_group, F.text) # TODO уйти от номеров в сторону название пачки
async def cmd_register_nickname(message: types.Message, state: FSMContext):
    try:
        game = await orm.GameOrm.get_game_by_number_group((int(message.text))) #await orm.get_game_by_number_group(message.text)
    except Exception as e: 
        await message.answer(f"Братан, ошибка получения номера игры, зови админа! Error: {e}" )
        

    if game is None:
        await message.answer("Але, тебя нагрели, такой пачки нет")
        await state.clear()
        new_player.clear()
        return

    new_player.game_id = int(message.text)
    await message.answer("Окей, а кликуха у тебя в пачке какая?")

    await state.update_data({"number_group": message.text})
    await state.set_state(states.RegisterState.nickname)

    logging.debug("Set state: states.RegisterState.nickname, data: %s", message.text)


@register_route.message(states.RegisterState.nickname)
async def cmd_register_done(message: types.Message, state: FSMContext):
    new_player.player_name = message.text
    await state.update_data({"nickname": message.text})

    data = await state.get_data()

    logging.debug("Set state: states.RegisterState.done. data: %s", data)
    if new_player.player_name is None or new_player.game_id is None:
        new_player.clear()
        await message.answer(
            f"Братан {message.from_user.full_name}! Ты слепой, данных не хватает! Давай по новой!"
        )
        await state.clear()

        cmd_register_number_group(message, state)
    else:
        await message.answer(
            f"Окей, добро пожаловать в мрачный мир будущего " f"{data['nickname']}!", reply_markup=keyboards.PlayerMenuButtons().get_keyboard()
        )
        try:
            await orm.PlayerOrm.update_new_player(new_player)
        except Exception as e:
            await message.answer(f"Братан {message.from_user.full_name}! У нас ошибка , пиши админу! Error: {e}")
            logging.error(f"Error: {e}")
        
    new_player.clear()
    await state.clear()
    
