"""Регистрация пользователей с использованием конечных автоматов.
Функции вызывается по очереди и записывает ответ из прошлой.
"""

from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases import models
import logging
from aiogram import F, Router, types

from pager.databases.requests.game import GameRequest
from pager.databases.requests.player import PlayerRequest
from pager.exeption.exeption import NotFoundError, handler_error


class Register:
    """Регистрация пользователей с использованием конечных автоматов."""

    register_route = Router()

    @staticmethod
    @register_route.message(F.text == "Зарегистрироваться")
    async def cmd_register_number_group(message: types.Message, state: FSMContext):
        """Запрашивает номер группы."""
        await message.answer("Назови номер группы")
        await state.update_data({"id_tg": message.from_user.id})
        await state.update_data({"username": message.from_user.username})
        await state.set_state(states.RegisterState.number_group)

    @staticmethod
    @register_route.message(states.RegisterState.number_group, F.text)
    async def cmd_register_nickname(message: types.Message, state: FSMContext):
        """Запрашивает ник в игре."""
        try:
            game = await GameRequest.get_game_by_number_group(
                (int(message.text))
            )  # await orm.get_game_by_number_group(message.text)
            state.update_data({"date": game.date})
        except NotFoundError:
            logging.warning("Не найдена группа! Попробуйте еще раз ввести!")
            return 
        except Exception as e:
            await handler_error(e, message, state, message.text)
            return
        
        await state.update_data({"game_id": int(message.text)})
        await message.answer("Какой ваш ник в игре?")
        await state.set_state(states.RegisterState.nickname)

    @staticmethod
    @register_route.message(states.RegisterState.nickname)
    async def cmd_register_done(message: types.Message, state: FSMContext):
        """Вносит данные в БД."""
        await state.update_data({"player_name": message.text})
        data = await state.get_data()
        if not data.get("player_name") or not data.get("game_id"):
            await message.answer(f"{message.from_user.full_name}! Не хватает данных, начни заново!")
            await state.clear()
            return
        new_player = models.Player(**data)
        try:
            await PlayerRequest.update_new_player(new_player)
        except Exception as e:
            await handler_error(e, message, state, message.text, data.get("player_name"))
            return

        await message.answer(
            f"Добро пожаловать {data['player_name']}, ближайшее время игры: {data['date']}",
            reply_markup=keyboards.PlayerMenuButtons().get_keyboard(),
        )
        await state.clear()
