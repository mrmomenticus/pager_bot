from aiogram import Router, types
from aiogram.filters.command import CommandStart
from pager import keyboards
from pager.databases import orm


start_route = Router()


@start_route.message(CommandStart())
async def cmd_start(message: types.Message):
    players = await orm.get_from_id(message.from_user.id) 
    if players is not None:
        await message.answer("<b>Рад видеть </b>" + players.player_name + "<b>, че тебе надо?</b>", parse_mode="html")
    else:
        await message.answer(
        "<b>Привет кусок мяса. Добро пожаловать в мрачный мир будущего! Тебе тут не рады, но любое мнение тут пыль. Чего ты хочешь?</b>",
        parse_mode="html",
        reply_markup=keyboards.registred_button,
        )
    
    # TODO: Добавить проверку на регистрацию пользователя. Если такого нет в базе данных, регистрировать его
