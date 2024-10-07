
import logging
from aiogram import F, Router, types

from pager import keyboards
from pager.databases.orm import PlayerOrm
from aiogram.types import FSInputFile

main_menu_players = Router()


class MainMenu:

    @staticmethod
    @main_menu_players.message(F.text == "Организация...")
    async def cmd_main_menu(message: types.Message):
        await message.answer(
            "Выберите действие", reply_markup=keyboards.PlayerOrganization().get_keyboard()
        )

    @staticmethod
    @main_menu_players.message(F.text == "Инвентарь и статы...")
    async def cmd_info_players(message: types.Message):
        await message.answer(
            "Что хотите?", reply_markup=keyboards.PlayerInventory().get_keyboard()
        )
    
    @staticmethod
    @main_menu_players.message(F.text == "Назад")
    async def cmd_main_menu_players(message: types.Message):
        await message.answer(
            "Выберите действие", reply_markup=keyboards.PlayerMenuButtons().get_keyboard()
        )
    
class Organization:
    @staticmethod
    @main_menu_players.message(F.text == "Когда игра?")
    async def cmd_when_game(message: types.Message):
        date = await PlayerOrm.select_games_by_player_id(message.from_user.id)
        if date is None:
            await message.answer("Даты игры не найдены")
        else:
            await message.answer(f"Игра будет: {date.date.strftime('%d.%m.%Y')}", reply_markup=keyboards.PlayerMenuButtons().get_keyboard())



class Inventory:
    @staticmethod
    @main_menu_players.message(F.text == "Мои статы")
    async def cmd_info_players(message: types.Message):
        player = await PlayerOrm.select_player_from_id(message.from_user.id)
        if player is None:
            await message.answer("Странно, но ваши данные не найдены")
        else:
            for photo in player.photo_state:
                try:
                    photo_file = FSInputFile(photo)
                    await message.answer_photo(photo_file)
                except Exception as e:
                    logging.error(f"Братан, пиши разрабу, у нас ошибка! Error: {e}")
                    await message.answer(f"Error: {e}")
                    
    @staticmethod
    @main_menu_players.message(F.text == "Мои вещи")
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
    @main_menu_players.message(F.text == "Мои деньги")
    async def cmd_money_players(message: types.Message):
        player = await PlayerOrm.select_player_from_id(message.from_user.id)
        money = await PlayerOrm.select_money(player.player_name)
        if player is None:
            await message.answer("Странно, но ваши данные не найдены")
        else:
            await message.answer(f"Ваш баланс: {money}")