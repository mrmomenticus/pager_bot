import asyncio
import logging

from config.config import cfg
from app.handler import route
from aiogram import Bot, Dispatcher



async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = Bot(token=cfg["token"])
    # Диспетчер
    dp = Dispatcher()
    logging.debug("Start polling")
    dp.include_router(route)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())