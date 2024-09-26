import logging
import os
from aiogram import F, Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases.orm import PlayerOrm, GameOrm
from pager.databases import core
import re

main_menu_admin = Router()

class MainMenu:
    @staticmethod
    @main_menu_admin.message(F.text == "Организация игры...")
    async def cmd_main_menu(message: types.Message):
        await message.answer(
            "Выберите действие", reply_markup=keyboards.AdminOrganization().get_keyboard()
        )
    
    @staticmethod
    @main_menu_admin.message(F.text == "Игра...")
    async def cmd_main_menu_game(message: types.Message):
        await message.answer(
            "Выберите действие", reply_markup=keyboards.AdminGame().get_keyboard()
        )
    
    @staticmethod
    @main_menu_admin.message(F.text == "Информация по игрокам...")
    async def cmd_main_menu_info_players(message: types.Message):
        await message.answer(
            "Выберите действие", reply_markup=keyboards.AdminInformationPlayer().get_keyboard()
        )
        
    @staticmethod
    @main_menu_admin.message(F.text == "Инвентарь игрока...")
    async def cmd_main_menu_inventory_players(message: types.Message):
        await message.answer(
            "Выберите действие", reply_markup=keyboards.AdminInventoryPlayers().get_keyboard()
        )
    
    @staticmethod
    @main_menu_admin.message(F.text == "Назад")
    async def cmd_back(message: types.Message):
        await message.answer(
           "Возвращаю", reply_markup=keyboards.AdminMenuButtons().get_keyboard()
      )
        

class DataGame:
    @staticmethod
    @main_menu_admin.message(F.text == "Добавить дату")
    async def cmd_number_group(message: types.Message, state: FSMContext):
        await message.answer("Введи номер пачки")

        await state.set_state(states.AddDateState.number_group)

    @staticmethod
    @main_menu_admin.message(states.AddDateState.number_group, F.text)
    async def cmd_register_date(message: types.Message, state: FSMContext):
        await message.answer("Введи дату в формате дд.мм.гггг")

        await state.set_data({"number_group": message.text})

        await state.set_state(states.AddDateState.date)

    @staticmethod
    @main_menu_admin.message(states.AddDateState.date, F.text)
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

        await state.clear()


class NewGroup:
    @staticmethod
    @main_menu_admin.message(F.text == "Добавить группу")
    async def cmd_add_group(message: types.Message, state: FSMContext):
        await message.answer("Введи номер группы")
        await state.set_state(states.AddGroupState.number_group)

    @staticmethod
    @main_menu_admin.message(states.AddGroupState.number_group, F.text)
    async def cmd_add_group_name(message: types.Message, state: FSMContext):
        await message.answer("Введи название группы")

        await state.set_data({"nubmer_game": message.text})

        await state.set_state(states.AddGroupState.group_name)

    @staticmethod
    @main_menu_admin.message(states.AddGroupState.group_name, F.text)
    async def cmd_success_add_group(message: types.Message, state: FSMContext):
        nubmer_game = await state.get_data()

        game = core.Game(
            number_group=int(nubmer_game["nubmer_game"]), game_name=message.text
        )

        await GameOrm.set_new_game(game)

        await message.answer(
            "Группа успешно добавлена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )

        await state.clear()


class InfoPlayers:
    @staticmethod
    @main_menu_admin.message(F.text == "Информация по игрокам...")
    async def cmd_info_players(message: types.Message):
        await message.answer(
            "Что хотите?", reply_markup=keyboards.AdminInformationPlayer().get_keyboard()
        )

    @staticmethod
    @main_menu_admin.message(F.text == "Добавить информацию")
    async def cmd_add_info(message: types.Message, state: FSMContext):
        await message.answer("Че за игрок?")

        await state.set_state(states.AddInfoState.name)

    @staticmethod
    @main_menu_admin.message(states.AddInfoState.name, F.text)
    async def cmd_add_photo(message: types.Message, state: FSMContext):
        await message.answer("Отправь фото стат игрока")

        await state.set_data({"name": message.text})

        await state.set_state(states.AddInfoState.photo)

    @staticmethod
    @main_menu_admin.message(states.AddInfoState.photo, F.photo)
    async def cmd_save_info(message: types.Message, state: FSMContext):
        name = (await state.get_data()).get("name")

        os.makedirs(os.path.join("images", name), exist_ok=True)

        await message.bot.download(
            message.photo[-1].file_id,
            f"images/{name}/{name}_{message.photo[-1].file_id}.jpg",
        )

        await PlayerOrm.create_photo_state(
            name, f"images/{name}/{name}_{message.photo[-1].file_id}.jpg"
        )

        await message.answer(
            "Информация успешно добавлена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )
        await state.clear()

    @staticmethod
    @main_menu_admin.message(F.text == "Получить информацию")
    async def cmd_get_name_for_info(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.GetInfoState.name)

    @staticmethod
    @main_menu_admin.message(states.GetInfoState.name, F.text)
    async def cmd_get_info(message: types.Message, state: FSMContext):
        player = await PlayerOrm.select_photo_state(message.text)

        if player is None:
            await message.answer("Такого игрока нет")
            return

        for player in player:
            for photo in player.photo_state:
                try:
                    photo_file = FSInputFile(photo)
                    await message.answer_photo(photo_file)
                except Exception as e:
                    logging.error(f"Братан, пиши разрабу, у нас ошибка! Error: {e}")
                    await message.answer(f"Error: {e}")
        await state.clear()

    @staticmethod
    @main_menu_admin.message(F.text == "Удалить информацию")
    async def cmd_delete_info_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.DeleteInfoState.name)

    @staticmethod
    @main_menu_admin.message(states.DeleteInfoState.name, F.text)
    async def cmd_delete_info(message: types.Message, state: FSMContext):
        await PlayerOrm.delete_photo_state(message.text)

        try:
            import shutil

            shutil.rmtree(f"images/{message.text}")
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"Братан, пиши разрабу, у нас ошибка! Error: {e}")
            await message.answer(f"Error: {e}")

        await message.answer(
            "Информация успешно удалена",
            reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
        )
        await state.clear()


class InventoryPlayers:
    @staticmethod
    @main_menu_admin.message(F.text == "Инвентарь игрока...")
    async def cmd_inventory_players(message: types.Message):
        await message.answer(
            "Что именно хотите?",
            reply_markup=keyboards.AdminInventoryPlayers().get_keyboard(),
        )

    @staticmethod
    @main_menu_admin.message(F.text == "Добавить денег")
    async def cmd_add_money_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.AddMoneyState.name)

    @staticmethod
    @main_menu_admin.message(states.AddMoneyState.name, F.text)
    async def cmd_add_money(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Количество денег")

        await state.set_state(states.AddMoneyState.money)

    @staticmethod
    @main_menu_admin.message(states.AddMoneyState.money, F.text)
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
    @main_menu_admin.message(F.text == "Забрать деньги")
    async def cmd_take_money_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.TakeMoneyState.name)

    @staticmethod
    @main_menu_admin.message(states.TakeMoneyState.name, F.text)
    async def cmd_take_money(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Количество денег")

        await state.set_state(states.TakeMoneyState.money)

    @staticmethod  # TODO Можем уйти в минус
    @main_menu_admin.message(states.TakeMoneyState.money, F.text)
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
    @main_menu_admin.message(F.text == "Добавить вещь")
    async def cmd_add_item_name_player(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.AddItemState.name_player)

    @staticmethod
    @main_menu_admin.message(states.AddItemState.name_player, F.text)
    async def cmd_add_item_name(message: types.Message, state: FSMContext):
        await state.update_data(name_player=message.text)
        await message.answer("Название вещи")

        await state.set_state(states.AddItemState.name_item)

    @staticmethod
    @main_menu_admin.message(states.AddItemState.name_item, F.text)
    async def cmd_add_item_price(message: types.Message, state: FSMContext):
        await state.update_data(name_item=message.text)
        await message.answer("Цена вещи")

        await state.set_state(states.AddItemState.price_item)

    @staticmethod
    @main_menu_admin.message(states.AddItemState.price_item, F.text)
    async def cmd_add_item_description(message: types.Message, state: FSMContext):
        await state.update_data(price_item=message.text)
        await message.answer("Описание вещи")

        await state.set_state(states.AddItemState.description)

    @staticmethod
    @main_menu_admin.message(states.AddItemState.description, F.text)
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
    @main_menu_admin.message(F.text == "Удалить вещь")
    async def cmd_delete_item_name_player(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.DeleteItemState.name_player)

    @staticmethod
    @main_menu_admin.message(states.DeleteItemState.name_player, F.text)
    async def cmd_delete_item_name(message: types.Message, state: FSMContext):
        await state.update_data(name_player=message.text)

        await message.answer("Название вещи")

        await state.set_state(states.DeleteItemState.name_item)

    @staticmethod
    @main_menu_admin.message(states.DeleteItemState.name_item, F.text)
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
    @main_menu_admin.message(F.text == "Узнать инвентарь игрока")
    async def cmd_all_inventory(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.AllInventoryPlayer.name_player)
        
    @staticmethod
    @main_menu_admin.message(states.AllInventoryPlayer.name_player, F.text)
    async def cmd_all_inventory_complete(message: types.Message, state: FSMContext):
        try:
            stuffs = await PlayerOrm.select_all_stuff(message.text)
            
            money = await PlayerOrm.select_money(message.text)
            
            await message.answer(f"Игрок {message.text} имеет: ")
            for stuff in stuffs:
                await message.answer(f"Название: {stuff.title}\nЦена: {stuff.price}\nОписание: {stuff.description}")
            await message.answer(f"А также сумму {money} денег")
            
        except ValueError as e:
            await message.answer(f"Братан пиши разрабу, у нас ошибка! Error: {e}")
        
    
