import asyncio
import logging

from pager.bot import BotManager
from pager.handlers import register, start, menu_admin, menu_players
from pager.databases import core


async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot_manager = BotManager()
    bot_manager.get_pager_bot().add_routes(
        [
            start.start_route,
            register.register_route,
            menu_admin.main_menu_admin,
            menu_players.main_menu_players,
        ]
    )    
    logging.debug("Start polling")

    await core.init_database()

    await bot_manager.start_bot()


if __name__ == "__main__":
    asyncio.run(main())
