from aiogram import F, types, Router
from pager.state import states
from pager.databases.requests.npc import NpcRequest
from pager.middleware.filter import Role
from aiogram.fsm.context import FSMContext

from pager.utils.globals import number_group
from keyboards import keyboards
from pager.notification.notification import Notification


class NpcAdmin:
    npc_route = Router()
    npc_route.message.filter(Role(is_admin=True))

    @staticmethod
    @npc_route.message(F.text == "Добавить NPC")
    async def cmd_add_group(message: types.Message, state: FSMContext):
        await message.answer("Имя NPC")
        await state.update_data(number_group=message.text)
        await state.set_state(states.NewNpcState.name)

    @staticmethod
    @npc_route.message(states.NewNpcState.name, F.text)
    async def cmd_add_local(message: types.Message, state: FSMContext):
        await message.answer("Локация нпс")
        await state.update_data(name=message.text)
        await state.set_state(states.NewNpcState.local)

    @staticmethod
    @npc_route.message(states.NewNpcState.local, F.text)
    async def cmd_add_description(message: types.Message, state: FSMContext):
        await message.answer("Описание нпс")
        await state.update_data(local=message.text)
        await state.set_state(states.NewNpcState.description)

    @staticmethod
    @npc_route.message(states.NewNpcState.description, F.text)
    async def cmd_npc_end(message: types.Message, state: FSMContext):
        await state.update_data(description=message.text)
        npc = await state.get_data()
        try:
            await NpcRequest.add_npc(npc=npc)
        except Exception:   
            await message.answer("Возникла ошибка. Попробуйте позже")
            await state.clear()
            return
        await message.answer(
            "NPC успешно добавлен",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )
        await Notification.notification_all_players(message_str="Новый знакомый: ", new_data=npc["name"])
        await state.clear()


class NpcPlayer:
    npc_route = Router()
    npc_route.message.filter(Role())

    @staticmethod
    @npc_route.message(F.text == "NPC")
    async def cmd_get_npc(message: types.Message):
        npcs= await NpcRequest.get_npcs(number_group=number_group)
        if not npcs:
            await message.answer("NPC не найдены")
        msg = "NPC в игре: \n"
        for npc in npcs:
            msg += f"Имя: {npc.name}\nЛокация: {npc.local}\nОписание: {npc.description}\n\n"
        await message.answer(msg)

        
        