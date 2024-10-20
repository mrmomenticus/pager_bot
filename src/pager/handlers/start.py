from aiogram import Router, types
from aiogram.filters.command import CommandStart
from pager import keyboards
from pager.databases.requests.player import PlayerRequest


start_route = Router()


@start_route.message(CommandStart())
async def cmd_start(message: types.Message):
    players = await PlayerRequest.select_player(message.from_user.id)
    if players is not None:
        if players.is_admin:
            await message.answer(
                "Рад видеть администратора " + players.player_name + ", че тебе надо?",
                reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
            )
        else:
            await message.answer(
                "Рад видеть " + players.player_name + " че тебе надо?",
                reply_markup=keyboards.PlayerMenuButtons().get_keyboard(),
            )
    else:
        await message.answer(
            "Добро пожаловать, тебя нет в базе данных, нажми кнопку регистрации",
            reply_markup=keyboards.RegistredButton().get_keyboard(),
        )
