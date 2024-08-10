import asyncio
import logging

from pager import configs
from aiogram import Bot, Dispatcher
from pager.handlers import register, start
from pager.databases import orm


async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = Bot(token=configs.cfg["token"])  # type: ignore
    # Диспетчер
    dp = Dispatcher()
    logging.debug("Start polling")

    dp.include_router(start.start_route)
    dp.include_router(register.register_route)

    await orm.insert_data()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
