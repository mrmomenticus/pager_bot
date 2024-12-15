from aiogram import F, Router, types
from pager import keyboards, states
from pager.filter import Role
from aiogram.fsm.context import FSMContext

from pager.commands.voting import Voting
from pager.utils.globals import number_group


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
    @route_admin.message(F.text == "Быстрое голосование")
    async def cmd_quick_voice(message: types.Message, state: FSMContext):
        await message.answer("Отправте вопрос")
        await state.set_state(states.QuickVoiceState.question)
    
    @staticmethod
    @route_admin.message(states.QuickVoiceState.question, F.text)
    async def cmd_voice_complete(message: types.Message, state: FSMContext):
        await state.update_data({"question": message.text})
        data = await state.get_data()
        await Voting().send_quick_poll(number_group, data["question"])
        state = await state.clear()

    @staticmethod
    @route_admin.message(F.text == "Данные игрока...")
    async def cmd_data_players(message: types.Message):
        await message.answer(
            "Выберите действие",
            reply_markup=keyboards.AdminDataPlayer().get_keyboard(),
        )

    @staticmethod
    @route_admin.message(F.text == "Назад")
    async def cmd_back(message: types.Message):
        await message.answer(
            "Возвращаю", reply_markup=keyboards.AdminMenuButtons().get_keyboard()
        )
