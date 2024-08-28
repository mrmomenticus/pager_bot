import logging
import os
from aiogram import F, Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from pager import keyboards, states
from pager.databases import orm
import re

main_menu_admin = Router()

"""Блок добавлениы времени"""


@main_menu_admin.message(F.text == "Добавить время игры")
async def cmd_number_group(message: types.Message, state: FSMContext):
    await message.answer("Введи номер пачки")

    await state.set_state(states.AddDateState.number_group)


@main_menu_admin.message(states.AddDateState.number_group, F.text)
async def cmd_register_date(message: types.Message, state: FSMContext):
    await message.answer("Введи дату в формате дд.мм.гггг")

    await state.set_data({"number_group": message.text})

    await state.set_state(states.AddDateState.date)


@main_menu_admin.message(states.AddDateState.date, F.text)
async def cmd_add_time(message: types.Message, state: FSMContext):
    pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$")
    if not pattern.match(message.text):
        await message.answer("Неверный формат даты, попробуй ещё раз.")
        return

    data = await state.get_data()
    await orm.set_date_game(int(data["number_group"]), message.text)

    await message.answer(
        "Дата успешно добавлена",
        reply_markup=keyboards.PlayerMenuButtons().get_keyboard(),
    )

    await state.clear()


# TODO: Отделить выше методы в отдельный класс


"""Блок добавлениы группы"""


@main_menu_admin.message(F.text == "Добавить группу")
async def cmd_add_group(message: types.Message, state: FSMContext):
    await message.answer("Введи номер группы")

    await state.set_state(states.AddGroupState.number_group)


@main_menu_admin.message(states.AddGroupState.number_group, F.text)
async def cmd_add_group_name(message: types.Message, state: FSMContext):
    await message.answer("Введи название группы")

    await state.set_data({"nubmer_game": message.text})

    await state.set_state(states.AddGroupState.group_name)


@main_menu_admin.message(states.AddGroupState.group_name, F.text)
async def cmd_success_add_group(message: types.Message, state: FSMContext):
    nubmer_game = await state.get_data()

    game = orm.Game(
        number_group=int(nubmer_game["nubmer_game"]), game_name=message.text
    )

    await orm.set_new_game(game)

    await message.answer(
        "Группа успешно добавлена",
        reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
    )

    await state.clear()


"""Блок информации по игрокам"""


@main_menu_admin.message(F.text == "Информация по игрокам...")
async def cmd_info_players(message: types.Message):
    await message.answer(
        "Что хотите?", reply_markup=keyboards.InformationPlayers().get_keyboard()
    )


@main_menu_admin.message(F.text == "Добавить информацию")
async def cmd_add_info(message: types.Message, state: FSMContext):
    await message.answer("Че за игрок?")

    await state.set_state(states.AddInfoState.name)


@main_menu_admin.message(states.AddInfoState.name, F.text)
async def cmd_add_photo(message: types.Message, state: FSMContext):
    await message.answer("Отправь фото стат игрока")

    await state.set_data({"name": message.text})

    await state.set_state(states.AddInfoState.photo)


@main_menu_admin.message(states.AddInfoState.photo, F.photo)
async def cmd_save_info(message: types.Message, state: FSMContext):
    name = (await state.get_data()).get("name")

    os.makedirs(os.path.join("images", name), exist_ok=True)

    await message.bot.download(
        message.photo[-1].file_id,
        f"images/{name}/{name}_{message.photo[-1].file_id}.jpg",
    )

    await orm.set_new_photo_state(
        name, f"images/{name}/{name}_{message.photo[-1].file_id}.jpg"
    )

    await message.answer(
        "Информация успешно добавлена",
        reply_markup=keyboards.AdminMenuButtons().get_keyboard(),
    )
    await state.clear()


@main_menu_admin.message(F.text == "Получить информацию")
async def cmd_get_name_for_info(message: types.Message, state: FSMContext):
    await message.answer("Отправте имя игрока")

    await state.set_state(states.GetInfoState.name)


@main_menu_admin.message(states.GetInfoState.name, F.text)
async def cmd_get_info(message: types.Message, state: FSMContext):
    player = await orm.get_photo_state(message.text)

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

@main_menu_admin.message(F.text == "Удалить информацию")
async def cmd_delete_info_name(message: types.Message, state: FSMContext):
    await message.answer("Отправте имя игрока")

    await state.set_state(states.DeleteInfoState.name)
    

@main_menu_admin.message(states.DeleteInfoState.name, F.text)
async def cmd_delete_info(message: types.Message, state: FSMContext):
    await orm.delete_info(message.text)

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
    

@main_menu_admin.message(F.text == "Назад")
async def cmd_back(message: types.Message):
    await message.answer(
        "Назад", reply_markup=keyboards.AdminMenuButtons().get_keyboard()
    )
