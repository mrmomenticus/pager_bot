import asyncio
import logging

from pager import configs
from aiogram import Bot, Dispatcher
from pager.handlers import register, start, menu_admin, menu_players
from pager.databases import core


async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = Bot(token=configs.cfg["token"])  # type: ignore
    # Диспетчер
    dp = Dispatcher()
    logging.debug("Start polling")

    dp.include_router(start.start_route)
    dp.include_router(register.register_route)
    dp.include_router(menu_admin.main_menu_admin)
    dp.include_router(menu_players.main_menu_players)


    await core.init_database()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
