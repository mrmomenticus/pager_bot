import logging
from aiogram import F, Router, types
from aiogram.filters.command import CommandStart
from pager.commands.base import BaseHandler
from keyboards import keyboards
from pager.databases.requests.player import PlayerRequest
from pager.utils.exeption import NotFoundError

# TODO:
# 1. Перенести все логику в один класс
# 2. Добавить логику регистрации админа
# 3. Добавить проверки для админов и игроков
# 4. Добавить middlewire
# 5. Улучшить логику исключений и логирования


class Start(BaseHandler):
    start_route = Router()
    commands = ["Я ГМ", "Я игрок"]

    @start_route.message(CommandStart())
    async def start_bot(self, message: types.Message):
        player = await PlayerRequest.select_player(message.from_user.id)
        if player is None:
            await message.answer(
                "Добро пожаловать! Этот бот создан чтобы упростить жизнь для любителей НРИ.", 
                reply_markup=keyboards.RegistredButton().get_keyboard(),
            )
        else:
            pass  # TODO: Добавить логику 
        
    @start_route.message(F.text.in_(commands))
    async def handler_text(self, message: types.Message):
        case = message.text
        if case == "Я ГМ":
            await message.answer(
                "Выберите действие", reply_markup=keyboards.AdminMenuButtons().get_keyboard()
            )
        elif case == "Я игрок":
            await message.answer(
                "Выберите действие", reply_markup=keyboards.PlayerMenuButtons().get_keyboard()
            )
        
        
