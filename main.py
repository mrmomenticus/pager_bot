import asyncio
import logging

from config.config import cfg
from app.handler import route
from aiogram import Bot, Dispatcher

# Объект бота
bot = Bot(token=cfg["token"])
# Диспетчер
dp = Dispatcher()

async def main():
    logging.debug("Start polling")
    dp.include_router(route)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())