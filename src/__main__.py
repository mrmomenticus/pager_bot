import asyncio
import logging
from pager.utils.logger import LoggerConfigurator

from pager.utils.bot import BotManager
from pager.utils.globals import number_group

from pager.databases.requests.base import BaseRequest
from pager.handlers import (
    register,
    start,
    menu_admin,
    menu_players,
    data,
    inventory,
    group,
    state,
    stuff,
    voting,
    npc
)


async def main():
    LoggerConfigurator().configure()
    logging.info("Start bot")
    # Объект бота
    bot_manager = BotManager()
    bot_manager.get_pager_bot().add_routes(
        [
            start.start_route,
            register.Register.register_route,
            menu_admin.MainMenu.route_admin,
            menu_players.MenuPlayers.route_players,
            data.DataAdmin.data_route,
            data.DataPlayer.data_route,
            inventory.InventoryAdmin.inventory_route,
            inventory.InventoryPlayer.inventory_route,
            group.GroupAdmin.group_router,
            state.StateAdmin.info_router,
            state.StatePlayer.info_router,
            stuff.StuffAdmin.stuff_route,
            stuff.StuffPlayer.stuff_route,
            voting.Voting.voiting_router,
            npc.NpcAdmin.npc_route,
            npc.NpcPlayer.npc_route
            
        ]
    )
    logging.debug("Start polling")
    await BaseRequest.init_database()

    await bot_manager.start_bot()


if __name__ == "__main__":
    asyncio.run(main())
    