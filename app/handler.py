
from aiogram import  Router, types
from aiogram.filters.command import CommandStart

route = Router()
@route.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Hello!")