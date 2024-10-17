from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases.requests.game import GameOrm
from pager.databases.requests.player import PlayerOrm
from pager.utils.bot import BotManager
import re
from pager.filter import IsAdmin

class DataAdmin:
    data_route = Router()
    data_route.message.filter(IsAdmin)

    @staticmethod
    async def _notification_group(number_group: int, message_str: str, new_data):
        bot_manager = BotManager()
        players = await GameOrm.get_players_from_game(number_group)
        for player in players:
            await (
                bot_manager.get_pager_bot()
                .get_raw_bot()
                .send_message(player.id_tg, f"{message_str}: {new_data}")
            )

    @staticmethod
    @data_route.message(F.text == "Добавить дату игры")
    async def cmd_number_group(message: types.Message, state: FSMContext):
        await message.answer("Введи номер пачки")
        await state.set_state(states.AddDateState.number_group)

    @staticmethod
    @data_route.message(states.AddDateState.number_group, F.text)
    async def cmd_register_date(message: types.Message, state: FSMContext):
        await message.answer("Введи дату в формате дд.мм.гггг")
        await state.set_data({"number_group": message.text})
        await state.set_state(states.AddDateState.date)

    @staticmethod
    @data_route.message(states.AddDateState.date, F.text)
    async def cmd_add_time(message: types.Message, state: FSMContext):
        pattern = re.compile(
            r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$"
        )
        if not pattern.match(message.text):
            await message.answer("Неверный формат даты, попробуй ещё раз.")
            return

        data = await state.get_data()

        await GameOrm.set_date_game(int(data["number_group"]), message.text)
        await message.answer(
            "Дата успешно добавлена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )
        await DataAdmin._notification_group(
            int(data["number_group"]), "Обновление даты игры", message.text
        )
        await state.clear()


class DataPlayer:
    data_route = Router()
    
    @staticmethod
    @data_route.message(F.text == "Когда игра?")
    async def cmd_when_game(message: types.Message):
        date = await PlayerOrm.select_games_by_player_id(message.from_user.id)
        if date is None:
            await message.answer("Даты игры не найдены")
        else:
            await message.answer(
                f"Игра будет: {date.date.strftime('%d.%m.%Y')}",
                reply_markup=keyboards.PlayerMenuButtons().get_keyboard(),
            )
