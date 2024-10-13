from sqlalchemy import select
from pager.databases.core import Core
from pager.databases.models import Inventory, Player

class InventoryOrm:
    @Core().connection
    @staticmethod
    async def update_money(session, player_name: str, money: int):
        async with session.begin():
            stmt = (
                select(Inventory)
                .join(Player, Inventory.player_id == Player.id_tg)
                .where(Player.player_name == player_name)
            )
            result = await session.execute(stmt)
            inventory = result.scalars().first()
            if inventory is not None:
                inventory.money += money
                await session.commit()
                return inventory.money
            else:
                raise Exception("Такого игрока нет")

    @Core().connection
    @staticmethod
    async def select_money(session, player_name: str):
        stmt = (
            select(Inventory)
            .join(Player, Inventory.player_id == Player.id_tg)
            .where(Player.player_name == player_name)
        )
        result = await session.execute(stmt)
        inventory = result.scalars().first()
        if inventory is not None:
            return inventory.money
        else:
            raise Exception("Такого игрока нет")
