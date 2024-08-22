
from aiogram import F, Router, types

from pager import keyboards
from pager.databases import orm

main_menu_players = Router()

@main_menu_players.message(F.text == "Когда игра?")
async def cmd_when_game(message: types.Message):
    date = await orm.get_games_by_player_id(message.from_user.id)
    if date.date is None:
        await message.answer("Даты игры не найдены")
    else:
        await message.answer(f"Игра будет: {date.date.strftime('%d.%m.%Y')}", reply_markup=keyboards.PlayerMenuButtons().get_keyboard())

