import logging
import os
from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases.orm import PlayerOrm
from aiogram.types import FSInputFile


class InfoAdmin:
    info_router = Router()

    @staticmethod
    @info_router.message(F.text == "Информация по игрокам...")
    async def cmd_info_players(message: types.Message):
        await message.answer(
            "Что хотите?",
            reply_markup=keyboards.AdminInformationPlayer().get_keyboard(),
        )

    @staticmethod
    @info_router.message(F.text == "Добавить информацию")
    async def cmd_add_info(message: types.Message, state: FSMContext):
        await message.answer("Че за игрок?")

        await state.set_state(states.AddInfoState.name)

    @staticmethod
    @info_router.message(states.AddInfoState.name, F.text)
    async def cmd_add_photo(message: types.Message, state: FSMContext):
        await message.answer("Отправь фото стат игрока")

        await state.set_data({"name": message.text})

        await state.set_state(states.AddInfoState.photo)

    @staticmethod
    @info_router.message(states.AddInfoState.photo, F.photo)
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
    @info_router.message(F.text == "Получить информацию")
    async def cmd_get_name_for_info(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.GetInfoState.name)

    @staticmethod
    @info_router.message(states.GetInfoState.name, F.text)
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
    @info_router.message(F.text == "Удалить информацию")
    async def cmd_delete_info_name(message: types.Message, state: FSMContext):
        await message.answer("Отправте имя игрока")

        await state.set_state(states.DeleteInfoState.name)

    @staticmethod
    @info_router.message(states.DeleteInfoState.name, F.text)
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


class InfoPlayer:
    info_router = Router()
    @staticmethod
    @info_router.message(F.text == "Мои статы")
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
    