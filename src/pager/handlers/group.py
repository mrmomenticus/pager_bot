from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases import models
from pager.databases.requests.game import GameRequest
from pager.utils.exeption import NotFoundError, handler_error
from pager.utils.utility import get_name_all_players_from_group
from pager.filter import Role
from pager.handlers.base import BaseHandler

class GroupAdmin(BaseHandler):
    group_router = Router()
    group_router.message.filter(Role(is_admin = True))

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

        await GameRequest.set_new_game(game)
        await message.answer(
            "Группа успешно добавлена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )
        await state.clear()


    @staticmethod
    @group_router.message(F.text == "Список игроков группы")
    async def cmd_players_in_group(message: types.Message, state: FSMContext):
        await message.answer("Введи номер группы")
        await state.set_state(states.OutputPlayersGroupState.number_group)
    
       
    @staticmethod
    @group_router.message(states.OutputPlayersGroupState.number_group, F.text)
    async def cmd_output_players_in_group(message: types.Message):
        try:
            await message.answer(await get_name_all_players_from_group(int(message.text)))
        except NotFoundError as e:
            await message.answer(f"{e}")
        except Exception as e:
            await handler_error(e, message, states, message.text)
