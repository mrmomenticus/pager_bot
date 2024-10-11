from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases import models
from pager.databases.orm import GameOrm

class GroupAdmin:
    group_router = Router()
    @staticmethod
    @group_router.message(F.text == "Добавить группу")
    async def cmd_add_group(message: types.Message, state: FSMContext):
        await message.answer("Введи номер группы")
        await state.set_state(states.AddGroupState.number_group)

    @staticmethod
    @group_router.message(states.AddGroupState.number_group, F.text)
    async def cmd_add_group_name(message: types.Message, state: FSMContext):
        await message.answer("Введи название группы")

        await state.set_data({"nubmer_game": message.text})

        await state.set_state(states.AddGroupState.group_name)

    @staticmethod
    @group_router.message(states.AddGroupState.group_name, F.text)
    async def cmd_success_add_group(message: types.Message, state: FSMContext):
        nubmer_game = await state.get_data()

        game = models.Game(
            number_group=int(nubmer_game["nubmer_game"]), game_name=message.text
        )

        await GameOrm.set_new_game(game)

        await message.answer(
            "Группа успешно добавлена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )

        await state.clear()
