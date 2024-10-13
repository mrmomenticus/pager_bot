from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases.requests.stuff import StuffOrm
from pager.databases.requests.player import PlayerOrm

class StuffAdmin:
    stuff_route = Router()
    @staticmethod
    @stuff_route.message(F.text == "Добавить вещь")
    async def add_item_name_player(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")
        await state.set_state(states.AddItemState.name_player)

    @staticmethod
    @stuff_route.message(states.AddItemState.name_player, F.text)
    async def add_item_name(message: types.Message, state: FSMContext):
        await state.update_data(name_player=message.text)
        await message.answer("Название вещи")
        await state.set_state(states.AddItemState.name_item)

    @staticmethod
    @stuff_route.message(states.AddItemState.name_item, F.text)
    async def add_item_price(message: types.Message, state: FSMContext):
        await state.update_data(name_item=message.text)
        await message.answer("Цена вещи")
        await state.set_state(states.AddItemState.price_item)

    @staticmethod
    @stuff_route.message(states.AddItemState.price_item, F.text)
    async def add_item_description(message: types.Message, state: FSMContext):
        await state.update_data(price_item=message.text)
        await message.answer("Описание вещи")
        await state.set_state(states.AddItemState.description)

    @staticmethod
    @stuff_route.message(states.AddItemState.description, F.text)
    async def add_item_complete(message: types.Message, state: FSMContext):
        await state.update_data(description=message.text)
        try:
            await StuffOrm().add_new_stuff(
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
    @stuff_route.message(F.text == "Удалить вещь")
    async def delete_item_name_player(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")
        await state.set_state(states.DeleteItemState.name_player)

    @staticmethod
    @stuff_route.message(states.DeleteItemState.name_player, F.text)
    async def delete_item_name(message: types.Message, state: FSMContext):
        await state.update_data(name_player=message.text)
        await message.answer("Название вещи")
        await state.set_state(states.DeleteItemState.name_item)

    @staticmethod
    @stuff_route.message(states.DeleteItemState.name_item, F.text)
    async def delete_item_complete(message: types.Message, state: FSMContext):
        try:
            await StuffOrm().delete_stuff(
                (await state.get_data()).get("name_player"), message.text
            )
            await message.answer(
                "Вещь успешно удалена",
                reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
            )
        except ValueError as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")


class StuffPlayer:
    stuff_route = Router()
    @staticmethod
    @stuff_route.message(F.text == "Мои вещи")
    async def cmd_stuff_players(message: types.Message):
        player = await PlayerOrm.select_player_from_id(message.from_user.id)
        stuffs = await StuffOrm().select_all_stuff(player.player_name)
        if player is None:
            await message.answer("Странно, но ваши данные не найдены")
        else:
            if stuffs is None:
                await message.answer("Ваших вещей нет")
            else:
                await message.answer("Ваши вещи: ")
                for stuff in stuffs:
                    await message.answer(
                        f"Название: {stuff.title}\nЦена: {stuff.price}\nОписание: {stuff.description}"
                    )