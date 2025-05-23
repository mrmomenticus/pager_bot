from aiogram import F, Router, types
from pager import keyboards
from pager.filter import Role

class MenuPlayers:
    route_players = Router()
    route_players.message.filter(Role())

    @staticmethod
    @route_players.message(F.text == "Организация...")
    async def cmd_main_menu(message: types.Message):
        await message.answer(
            "Выберите действие",
            reply_markup=keyboards.PlayerOrganization().get_keyboard(),
        )

    @staticmethod
    @route_players.message(F.text == "Инвентарь и статы...")
    async def cmd_info_players(message: types.Message):
        await message.answer(
            "Что хотите?", reply_markup=keyboards.PlayerInventory().get_keyboard()
        )
    
    @staticmethod
    @route_players.message(F.text == "Игра...")
    async def cmd_game_players(message: types.Message):
        await message.answer(
            "Выберите действие",
            reply_markup=keyboards.PlayerGame().get_keyboard(),
        )

    @staticmethod
    @route_players.message(F.text == "Назад")
    async def cmd_main_menu_players(message: types.Message):
        await message.answer(
            "Выберите действие",
            reply_markup=keyboards.PlayerMenuButtons().get_keyboard(),
        )
