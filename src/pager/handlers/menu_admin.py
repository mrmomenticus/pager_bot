from aiogram import F, Router, types
from pager import keyboards
from pager.filter import Role


class MainMenu:
    route_admin = Router()
    route_admin.message.filter(Role(is_admin=True))

    @staticmethod
    @route_admin.message(F.text == "Организация игры...")
    async def cmd_organization(message: types.Message):
        await message.answer(
            "Выберите действие",
            reply_markup=keyboards.AdminOrganization().get_keyboard(),
        )

    @staticmethod
    @route_admin.message(F.text == "Игра...")
    async def cmd_game(message: types.Message):
        await message.answer(
            "Выберите действие", reply_markup=keyboards.AdminGame().get_keyboard()
        )

    @staticmethod
    @route_admin.message(F.text == "Информация по игрокам...")
    async def cmd_info_players(message: types.Message):
        await message.answer(
            "Выберите действие",
            reply_markup=keyboards.AdminInformationPlayer().get_keyboard(),
        )

    @staticmethod
    @route_admin.message(F.text == "Инвентарь игрока...")
    async def cmd_inventory_players(message: types.Message):
        await message.answer(
            "Выберите действие",
            reply_markup=keyboards.AdminInventoryPlayers().get_keyboard(),
        )

    @staticmethod
    @route_admin.message(F.text == "Назад")
    async def cmd_back(message: types.Message):
        await message.answer(
            "Возвращаю", reply_markup=keyboards.AdminMenuButtons().get_keyboard()
        )
