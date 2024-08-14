
from aiogram import F, Router, types

from pager.databases import orm

main_menu_admin = Router()

@main_menu_admin.message(F.text == "Добавить время игры")
async def cmd_when_game(message: types.Message):
    date = await orm.get_games_by_player_id(message.from_user.id)
    
    await message.answer(f"Игра будет: {date.date.strftime('%d.%m.%Y')}")

