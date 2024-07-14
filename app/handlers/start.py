
import logging
from aiogram import  F, Router, types
from aiogram.filters.command import CommandStart, Command
from app.keyboards.keyboards import registred_button



start_route = Router()
@start_route.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("<b>Привет кусок мяса. Добро пожаловать в мрачный мир будущего! Тебе тут не рады, но любое мнение тут пыль. Чего ты хочешь?</b>",
                         parse_mode="html", reply_markup=registred_button)    
    #TODO: Добавить проверку на регистрацию пользователя. Если такого нет в базе данных, регистрировать его

