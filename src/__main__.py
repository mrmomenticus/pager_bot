import asyncio
import logging

from pager.bot import BotManager
from pager.handlers import register, start, menu_admin, menu_players, data, inventory, group, state
from pager.databases import models


async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot_manager = BotManager()
    bot_manager.get_pager_bot().add_routes(
        [
            start.start_route,
            register.register_route,
            menu_admin.MainMenu.route_admin,
            menu_players.MenuPlayers.route_players,
            data.DataAdmin.data_route,
            data.DataPlayer.data_route,
            inventory.InventoryAdmin.inventory_route,
            inventory.InventoryPlayer.inventory_player,
            group.GroupAdmin.group_router,
            state.StateAdmin.info_router,
            state.StatePlayer.info_router
        ]
    )    
    logging.debug("Start polling")

    await models.Core().init_database()

    await bot_manager.start_bot()


if __name__ == "__main__":
    asyncio.run(main())
