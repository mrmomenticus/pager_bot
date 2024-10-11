import logging
from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases.orm import PlayerOrm
class InventoryAdmin:
    inventory_route = Router()
    @staticmethod
    @inventory_route.message(F.text == "Инвентарь игрока...")
    async def cmd_inventory_players(message: types.Message):
        await message.answer(
            "Что именно хотите?",
            reply_markup=keyboards.AdminInventoryPlayers().get_keyboard(),
        )

    @staticmethod
    @inventory_route.message(F.text == "Добавить денег")
    async def cmd_add_money_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.AddMoneyState.name)

    @staticmethod
    @inventory_route.message(states.AddMoneyState.name, F.text)
    async def cmd_add_money(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Количество денег")

        await state.set_state(states.AddMoneyState.money)

    @staticmethod
    @inventory_route.message(states.AddMoneyState.money, F.text)
    async def cmd_add_money_complete(message: types.Message, state: FSMContext):
        name = (await state.get_data()).get("name")
        try:
            money = await PlayerOrm.update_money(name, int(message.text))
            if money is None:
                await message.answer(f"Игрок {name} не найден!")
            else:
                await message.answer(f"Игрок {name} имеет {money}!")
                await state.clear()
        except Exception as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")

    @staticmethod
    @inventory_route.message(F.text == "Забрать деньги")
    async def cmd_take_money_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.TakeMoneyState.name)

    @staticmethod
    @inventory_route.message(states.TakeMoneyState.name, F.text)
    async def cmd_take_money(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Количество денег")

        await state.set_state(states.TakeMoneyState.money)

    @staticmethod  # TODO Можем уйти в минус
    @inventory_route.message(states.TakeMoneyState.money, F.text)
    async def cmd_take_money_complete(message: types.Message, state: FSMContext):
        name = (await state.get_data()).get("name")
        try:
            money = await PlayerOrm.take_money(name, int(message.text))
            if money is None:
                await message.answer(f"Игрок {name} не найден!")
            else:
                await message.answer(f"Игрок {name} имеет {money}!")
        except Exception as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")

    @staticmethod
    @inventory_route.message(F.text == "Добавить вещь")
    async def cmd_add_item_name_player(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.AddItemState.name_player)

    @staticmethod
    @inventory_route.message(states.AddItemState.name_player, F.text)
    async def cmd_add_item_name(message: types.Message, state: FSMContext):
        await state.update_data(name_player=message.text)
        await message.answer("Название вещи")

        await state.set_state(states.AddItemState.name_item)

    @staticmethod
    @inventory_route.message(states.AddItemState.name_item, F.text)
    async def cmd_add_item_price(message: types.Message, state: FSMContext):
        await state.update_data(name_item=message.text)
        await message.answer("Цена вещи")

        await state.set_state(states.AddItemState.price_item)

    @staticmethod
    @inventory_route.message(states.AddItemState.price_item, F.text)
    async def cmd_add_item_description(message: types.Message, state: FSMContext):
        await state.update_data(price_item=message.text)
        await message.answer("Описание вещи")

        await state.set_state(states.AddItemState.description)

    @staticmethod
    @inventory_route.message(states.AddItemState.description, F.text)
    async def cmd_add_item_complete(message: types.Message, state: FSMContext):
        await state.update_data(description=message.text)
        try:
            await PlayerOrm.add_new_stuff(
                (await state.get_data()).get("name_player"),
                (await state.get_data()).get("name_item"),
                int((await state.get_data()).get("price_item")),
                (await state.get_data()).get("description"),
            )
        except Exception as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")
        await message.answer(
            "Вещь успешно добавлена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )
        await state.clear()

    @staticmethod
    @inventory_route.message(F.text == "Удалить вещь")
    async def cmd_delete_item_name_player(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.DeleteItemState.name_player)

    @staticmethod
    @inventory_route.message(states.DeleteItemState.name_player, F.text)
    async def cmd_delete_item_name(message: types.Message, state: FSMContext):
        await state.update_data(name_player=message.text)

        await message.answer("Название вещи")

        await state.set_state(states.DeleteItemState.name_item)

    @staticmethod
    @inventory_route.message(states.DeleteItemState.name_item, F.text)
    async def cmd_delete_item_complete(message: types.Message, state: FSMContext):
        try:
            await PlayerOrm.delete_stuff(
                (await state.get_data()).get("name_player"), message.text
            )
            await message.answer(
                "Вещь успешно удалена",
                reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
            )
        except ValueError as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")

    @staticmethod
    @inventory_route.message(F.text == "Узнать инвентарь игрока")
    async def cmd_all_inventory(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.AllInventoryPlayer.name_player)

    @staticmethod
    @inventory_route.message(states.AllInventoryPlayer.name_player, F.text)
    async def cmd_all_inventory_complete(message: types.Message, state: FSMContext):
        try:
            stuffs = await PlayerOrm.select_all_stuff(message.text)

            money = await PlayerOrm.select_money(message.text)

            await message.answer(f"Игрок {message.text} имеет: ")
            for stuff in stuffs:
                await message.answer(
                    f"Название: {stuff.title}\nЦена: {stuff.price}\nОписание: {stuff.description}"
                )
            await message.answer(f"А также сумму {money} денег")

        except ValueError as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")



class InventoryPlayer:
    inventory_player = Router()
                    
    @staticmethod
    @inventory_player.message(F.text == "Мои вещи")
    async def cmd_stuff_players(message: types.Message):
        try:
            player = await PlayerOrm.select_player_from_id(message.from_user.id)
            stuffs = await PlayerOrm.select_all_stuff(player.player_name)
        except Exception as e:
            logging.error(f"Error: {e}, id {message.from_user.id}")
            return await message.answer("Возникли проблемы. Обратись к @Mrmomenticus")
        if player is None:
            await message.answer("Странно, но ваши данные не найдены")
        else:
            if stuffs is None:
                await message.answer("Ваших вещей нет")
            else:
                await message.answer("Ваши вещи: ")
                for stuff in stuffs:
                    await message.answer(f"Название: {stuff.title}\nЦена: {stuff.price}\nОписание: {stuff.description}")
                
    @staticmethod
    @inventory_player.message(F.text == "Мои деньги")
    async def cmd_money_players(message: types.Message):
        player = await PlayerOrm.select_player_from_id(message.from_user.id)
        money = await PlayerOrm.select_money(player.player_name)
        if player is None:
            await message.answer("Странно, но ваши данные не найдены")
        else:
            await message.answer(f"Ваш баланс: {money}")