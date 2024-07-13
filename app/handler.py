
import logging
from aiogram import  F, Router, types
from aiogram.filters.command import CommandStart, Command
from app.keyboards import register_keyboard



route = Router()
@route.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("<b>Привет кусок мяса. Добро пожаловать в мрачный мир будущего! Тебе тут не рады, но любое мнение тут пыль. Чего ты хочешь?</b>",
                         parse_mode="html", reply_markup=register_keyboard())    
    #TODO: Добавить проверку на регистрацию пользователя. Если такого нет в базе данных, регистрировать его


@route.message(F.text == "Зарегистрироваться")
async def cmd_register(message: types.Message):
    
    