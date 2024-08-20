from aiogram import Router, types
from aiogram.filters.command import CommandStart
from pager import keyboards
from pager.databases import orm


start_route = Router()


@start_route.message(CommandStart())
async def cmd_start(message: types.Message):
    players = await orm.get_player_from_id(message.from_user.id)
    if players is not None:
        if players.is_admin:
            await message.answer(
                "Рад видеть администратора" + players.player_name + ", че тебе надо?",
                reply_markup=keyboards.main_menu_admin,
            )
        else:
            await message.answer(
                "Рад видеть " + players.player_name + "<b>, че тебе надо?",
                reply_markup=keyboards.main_menu_players,
            )
    else:
        await message.answer(
            "Привет кусок мяса. Добро пожаловать в мрачный мир будущего! Тебе тут не рады, но любое мнение тут пыль. Чего ты хочешь?",
            reply_markup=keyboards.registred_button,
        )
