import asyncio
from doctest import debug
from venv import logger
import aiogram 
import logging

from config.config import cfg
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)


# Объект бота
bot = Bot(token=cfg["token"])
# Диспетчер
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")
    
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Help!")

# Запуск процесса поллинга новых апдейтов
async def main():
    logging.debug("Start polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())