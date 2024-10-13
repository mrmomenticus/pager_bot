"""Регистрация пользователей с использованием конечных автоматов.
Функции вызывается по очереди и записывает ответ из прошлой.
"""

from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases import models
import logging
from aiogram import F, Router, types

from pager.databases.requests.game import GameOrm
from pager.databases.requests.player import PlayerOrm

register_route = Router()
new_player = models.Player()


@register_route.message(F.text == "Зарегистрироваться")
async def cmd_register_number_group(message: types.Message, state: FSMContext):
    new_player.id_tg = message.from_user.id
    new_player.username = message.from_user.username
    await message.answer("Назови номер группы")

    await state.set_state(states.RegisterState.number_group)

    logging.debug(
        "Set state: states.RegisterState.number_group, data: %s", message.text
    )


@register_route.message(
    states.RegisterState.number_group, F.text
)  # TODO уйти от номеров в сторону название пачки
async def cmd_register_nickname(message: types.Message, state: FSMContext):
    try:
        game = await GameOrm.get_game_by_number_group(
            (int(message.text))
        )  # await orm.get_game_by_number_group(message.text)
    except Exception as e:
        logging.error(f"Error: {e}, id {message.from_user.id}")
        await message.answer("Возникли проблемы. Обратись к @Mrmomenticus")

    if game is None:
        await message.answer("Такой группы нет")
        await state.clear()
        new_player.clear()
        return

    new_player.game_id = int(message.text)
    await message.answer("Какой ваш ник в игре?")

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
        await message.answer(f"{message.from_user.full_name}! Не хватает данных!")
        await state.clear()

        cmd_register_number_group(message, state)
    else:
        await message.answer(
            f"Добро пожаловать " f"{data['nickname']}!",
            reply_markup=keyboards.PlayerMenuButtons().get_keyboard(),
        )
        try:
            await PlayerOrm.update_new_player(new_player)
        except Exception as e:
            await message.answer("Возникли проблемы. Обратись к @Mrmomenticus")
            logging.error(f"Error: {e}")

    new_player.clear()
    await state.clear()
