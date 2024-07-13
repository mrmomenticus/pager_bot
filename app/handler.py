
from aiogram import  Router, types
from aiogram.filters.command import CommandStart, Command


route = Router()
@route.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет кусок мяса.")
    await message.reply("Ты кто?")
    await message.

