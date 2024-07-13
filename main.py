import asyncio
import logging

from config.config import cfg
from app.handlers.start import start_route
from aiogram import Bot, Dispatcher
from app.handlers.register import register_route


async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = Bot(token=cfg["token"])
    # Диспетчер
    dp = Dispatcher()
    logging.debug("Start polling")
    
    dp.include_router(start_route)
    dp.include_router(register_route)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())