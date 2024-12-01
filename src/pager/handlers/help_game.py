
import logging
import os
from aiogram import F, types, Router
from pager import keyboards, states
from pager.databases.requests.help_game import HelpGameRequest
from pager.databases.requests.game import GameRequest
from pager.filter import Role
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from pager.utils.globals import number_group
from pager.utils.notification import Notification


class HelpGameAdmin:
    help_route = Router()
    help_route.message.filter(Role(is_admin=True))
    
    @staticmethod
    @help_route.message(F.text == "Справка...")
    async def help_game(message: types.Message):
        await message.answer("Выберите действие", reply_markup=keyboards.AdminHelp().get_keyboard())
        
    @staticmethod
    @help_route.message(F.text == "Добавить материалы")
    async def add_materials(message: types.Message, state: FSMContext):
        await message.answer("Отправте материала")
        await state.set_state(states.AddHelpState.help)
        
    @staticmethod
    @help_route.message(states.AddHelpState.help, F.photo | F.document) 
    async def add_materials_end(message: types.Message, state: FSMContext):
        game_name = (await GameRequest.get_game_by_number_group(number_group)).game_name
        logging.info(game_name)
        os.makedirs(os.path.join("materials", game_name), exist_ok=True)

        if message.document:
            await message.bot.download(
                message.document.file_id,
                f"materials/{game_name}/{game_name}_{message.document.file_id}.pdf",
            )

            await HelpGameRequest.add_help(
                f"materials/{game_name}/{game_name}_{message.document.file_id}.pdf"
            )

            await message.answer(
                "Информация успешно добавлена",
                reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
            )
            await Notification.notification_all_players(message_str="Добавлен справочный материал.")
            await state.clear()
            return
        
        if message.photo:
            await message.bot.download(
                message.photo[-1].file_id,
                f"materials/{game_name}/{game_name}_{message.photo[-1].file_id}.jpg",
            )

            await HelpGameRequest.add_help(
                f"materials/{game_name}/{game_name}_{message.photo[-1].file_id}.jpg"
            )

            await message.answer(
                "Информация успешно добавлена",
                reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
            )

            await Notification.notification_all_players(message_str="Добавлен справочный материал.")
            await state.clear()
        else:
            await message.answer("Не найден файл или фото", reply_markup=keyboards.AdminMenuButtons().get_keyboard())
            await state.clear()

    @staticmethod
    @help_route.message(F.text == "Список материалов")
    async def show_help(message: types.Message):
        help = await HelpGameRequest.get_help(number_group)
        for i in help:
            try:
                help_file = FSInputFile(i.path)
                await message.answer_document(help_file)
            except Exception as e:
                logging.error(f"{e} + photo: {i}")
                await message.answer("Возникла ошибка. Попробуйте позже")
         
        
        
        
class HelpGamePlayer:
    help_route = Router()
    help_route.message.filter(Role())
    
    
    @staticmethod
    @help_route.message(F.text == "Материалы игры")
    async def help_game(message: types.Message):
        help = await HelpGameRequest.get_help(number_group)
        for i in help:
            try:
                help_file = FSInputFile(i.path)
                await message.answer_document(help_file)
            except Exception as e:
                logging.error(f"{e} + photo: {i}")
                await message.answer("Возникла ошибка. Попробуйте позже")



        
        