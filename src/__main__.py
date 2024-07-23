import asyncio
import logging

from cyberpunk_pager import configs
from aiogram import Bot, Dispatcher
from cyberpunk_pager.handlers import register, start


async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = Bot(token=configs.cfg["token"]) # type: ignore
    # Диспетчер
    dp = Dispatcher()
    logging.debug("Start polling")

    dp.include_router(start.start_route)
    dp.include_router(register.register_route)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
