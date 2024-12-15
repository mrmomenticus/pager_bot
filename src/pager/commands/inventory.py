import logging
from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases.requests.inventory import InventoryRequest
from pager.databases.requests.player import PlayerRequest
from pager.databases.requests.stuff import StuffRequest
from pager.filter import Role
from pager.commands.base import BaseHandler
from pager.utils.notification import Notification


class InventoryAdmin(BaseHandler):
    inventory_route = Router()
    inventory_route.message.filter(Role(is_admin=True))

    @staticmethod
    @inventory_route.message(F.text == "Инвентарь игрока...")
    async def get_inventory_player(message: types.Message):
        await message.answer(
            "Что именно хотите?",
            reply_markup=keyboards.AdminInventoryPlayers().get_keyboard(),
        )

    @staticmethod
    @inventory_route.message(F.text == "Добавить денег")
    async def add_money_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")
        await state.set_state(states.AddMoneyState.name)

    @staticmethod
    @inventory_route.message(states.AddMoneyState.name, F.text)
    async def add_money(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Количество денег")
        await state.set_state(states.AddMoneyState.money)

    @staticmethod
    @inventory_route.message(states.AddMoneyState.money, F.text)
    async def add_money_complete(message: types.Message, state: FSMContext):
        name = (await state.get_data()).get("name")
        try:
            money = await InventoryRequest.update_money(player_name=name, money= int(message.text))
            if money is None:
                await message.answer(f"Игрок {name} не найден!")
                state.clear()
            else:
                await message.answer(f"Игрок {name} имеет {money}!")
                await Notification.notification_player(player_data=name, message_str="Обновление денег, теперь: ", new_data=money)
                await state.clear()
        except Exception as e:
            logging.error(f"Ошибка: {e}, traceback: {e.__traceback__}, message: {message.text}")
            await message.answer("Возникла ошибка. Попробуйте позже")

    @staticmethod
    @inventory_route.message(F.text == "Забрать деньги")
    async def take_money_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")
        await state.set_state(states.TakeMoneyState.name)

    @staticmethod
    @inventory_route.message(states.TakeMoneyState.name, F.text)
    async def take_money(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Количество денег")
        await state.set_state(states.TakeMoneyState.money)

    @staticmethod
    @inventory_route.message(states.TakeMoneyState.money, F.text)
    async def take_money_complete(message: types.Message, state: FSMContext):
        name = (await state.get_data()).get("name")
        try:
            money = await InventoryRequest.take_money(player_name=name, money= int(message.text))
            if money is None:
                await message.answer(f"Игрок {name} не найден!")
            else:
                await message.answer(f"Игрок {name} имеет {money}!")
        except Exception as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")


    @staticmethod
    @inventory_route.message(F.text == "Узнать инвентарь игрока")
    async def all_inventory(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")
        await state.set_state(states.AllInventoryPlayer.name_player)

    @staticmethod
    @inventory_route.message(states.AllInventoryPlayer.name_player, F.text)
    async def all_inventory_complete(message: types.Message, state: FSMContext):
        try:
            stuffs = await StuffRequest.select_all_stuff(message.text)

            money = await InventoryRequest.select_money(message.text)

            await message.answer(f"Игрок {message.text} имеет: ")
            for stuff in stuffs:
                await message.answer(
                    f"Название: {stuff.title}\nЦена: {stuff.price}\nОписание: {stuff.description}"
                )
            await message.answer(f"А также сумму {money} денег")

            
        except ValueError as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")


class InventoryPlayer:
    inventory_route = Router()
    inventory_route.message.filter(Role)

    @staticmethod
    @inventory_route.message(F.text == "Мои деньги")
    async def cmd_money_players(message: types.Message):
        player = await PlayerRequest.select_player(message.from_user.id)
        money = await InventoryRequest.select_money(player.player_name)
        if player is None:
            await message.answer("Странно, но ваши данные не найдены")
        else:
            await message.answer(f"Ваш баланс: {money}")
