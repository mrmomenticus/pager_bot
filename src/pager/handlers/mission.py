from aiogram import F, types, Router
from pager import keyboards, states
from pager.databases.requests.mission import MissionRequest
from pager.filter import Role
from aiogram.fsm.context import FSMContext

from pager.utils.globals import number_group


class MissionAdmin:
    mission_route = Router()
    mission_route.message.filter(Role(is_admin=True))

    @staticmethod
    @mission_route.message(F.text == "Добавить задание")
    async def cmd_add_mission(message: types.Message, state: FSMContext):
        await message.answer("Локация миссии")
        await state.set_state(states.AddMissionState.local)

    @staticmethod
    @mission_route.message(states.AddMissionState.local, F.text)
    async def cmd_add_description(message: types.Message, state: FSMContext):
        await message.answer("Описание")
        await state.update_data(local=message.text)
        await state.set_state(states.AddMissionState.description)

    @staticmethod
    @mission_route.message(states.AddMissionState.description, F.text)
    async def cmd_reward(message: types.Message, state: FSMContext):
        await message.answer("Награда")
        await state.update_data(description=message.text)
        await state.set_state(states.AddMissionState.reward)
        
    @staticmethod
    @mission_route.message(states.AddMissionState.reward, F.text)
    async def cmd_mission_end(message: types.Message, state: FSMContext):
        await state.update_data(reward=message.text)
        mission = await state.get_data()
        try:
            await MissionRequest.add_mission(mission=mission)
        except Exception as e:   
            await message.answer(f"error: {e}")
            await state.clear()
            return
        await message.answer(
            "Миссия успешно добавлена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )
        await state.clear()
        
class MissionPlayer:
    mission_route = Router()
    mission_route.message.filter(Role())

    @staticmethod
    @mission_route.message(F.text == "Задания")
    async def cmd_get_npc(message: types.Message):
        missions= await MissionRequest.get_missions(number_group)
        if not missions:
            await message.answer("Миссий нет")
        msg = "Миссии в работе: \n"
        for mission in missions:
            msg += f"Локация: {mission.local}\nОписание: {mission.desctription}\nНаграда: {mission.reward}\n\n"
        await message.answer(msg)

        
        