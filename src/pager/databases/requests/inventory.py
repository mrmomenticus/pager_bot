from sqlalchemy import select
from pager.databases.models import Inventory, Player
from pager.databases.requests.base import BaseRequest


class InventoryRequest(BaseRequest[Inventory]):
    @BaseRequest.connection
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
                m = inventory.money
                await session.commit()
                return m
            else:
                session.rollback()
                raise Exception("Такого игрока нет")

    @BaseRequest.connection
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

    @BaseRequest.connection
    @staticmethod
    async def take_money(session, player_name: str, money: int):
        async with session.begin():
            stmt = (
                select(Inventory)
                .join(Player, Inventory.player_id == Player.id_tg)
                .where(Player.player_name == player_name)
            )
            result = await session.execute(stmt)
            inventory = result.scalars().first()
            if inventory is not None:
                sum = inventory.money - money
                inventory.money -= money
                await session.commit()
                return sum
            else:
                return None
