import asyncio
import logging
from pager.utils.logger import LoggerConfigurator

from pager.bot.bot import BotManager

from pager.databases.requests.base import BaseRequest
from pager.commands import (
    start   
)


async def main():
    LoggerConfigurator().configure()
    logging.info("Start bot")
    # Объект бота
    bot_manager = BotManager()
    bot_manager.get_pager_bot().add_routes(
        [
            start.Start.start_route,
        ]
    )
    await BaseRequest.init_database()
    logging.debug("Database initialized")
    await bot_manager.start_bot()
    logging.debug("Start polling")

if __name__ == "__main__":
    asyncio.run(main())
    