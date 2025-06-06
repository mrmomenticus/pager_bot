from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases.requests.game import GameRequest
from pager.utils.exeption import NotFoundError
from pager.commands.base import BaseHandler
import re
from pager.filter import Role
from pager.utils.notification import Notification

class DataAdmin(BaseHandler):
    data_route = Router()
    data_route.message.filter(Role(is_admin=True))
    
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
        try:
            await GameRequest.set_date_game(int(data["number_group"]), message.text)
            await message.answer(
                "Дата успешно добавлена",
                reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
            )
            #TODO: Раскомментировать 
            # await Notification.notification_group(
            #     int(data["number_group"]), "Обновление даты игры", message.text
            # )
            await Notification.notification_group_date(1, message.text)
            await state.clear()
        except NotFoundError as e:
            await message.answer(f"{e}")
        except Exception:
            message.answer("Ошибка запроса. Попробуйте позже или обратитесь к разработчику.")


class DataPlayer:
    data_route = Router()
    data_route.message.filter(Role)
    
    @staticmethod
    @data_route.message(F.text == "Когда игра?")
    async def cmd_when_game(message: types.Message):
        game = await GameRequest.select_game_by_player_id(message.from_user.id)
        if game.date is None:
            await message.answer("Даты игры не найдены")
        else:
            await message.answer(
                f"Игра будет: {game.date.strftime('%d.%m.%Y')}",
                reply_markup=keyboards.PlayerMenuButtons().get_keyboard(),
            )
