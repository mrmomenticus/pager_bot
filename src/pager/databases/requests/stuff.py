import logging
from sqlalchemy import select
from pager.databases.models import Inventory, Player, Stuff, Base
from pager.exeption import NotFoundError
from sqlalchemy.exc import SQLAlchemyError

class StuffOrm:
    @Base().connection
    @staticmethod
    async def add_new_stuff(
        session, player_name: str, item_name: str, price_item: int, description: str
    ):
        stmt = (
            select(Stuff)
            .join(Inventory)
            .join(Player)
            .where(Player.player_name == player_name)
            .where(Stuff.title == item_name)
        )
        result = await session.execute(stmt)
        stuff = result.scalars().first()
        if stuff is not None:
            raise ValueError("Такой предмет уже есть у данного игрока")
        else:
            stmt = (
                select(Inventory)
                .join(Player, Inventory.player_id == Player.id_tg)
                .where(Player.player_name == player_name)
            )
            result = await session.execute(stmt)
            inventory = result.scalars().first()
            if inventory is not None:
                session.add(
                    Stuff(
                        invetory_id=inventory.id,
                        title=item_name,
                        price=price_item,
                        description=description,
                    )
                )
            else:
                raise SQLAlchemyError("Такого игрока нет")
            await session.commit()

    @Base().connection
    @staticmethod
    async def delete_stuff(session, name_player: str, name_item: str):
        async with session.begin():
            try:
                stmt = (
                    select(Stuff)
                    .join(Inventory, Stuff.invetory_id == Inventory.id)
                    .join(Player, Inventory.player_id == Player.id_tg)
                    .where(Player.player_name == name_player, Stuff.title == name_item)
                )
                result = await session.execute(stmt)
                stuff = result.scalars().first()
                if stuff is not None:
                    await session.delete(stuff)
                else:
                    raise NotFoundError(Stuff.__tablename__, name_item, name_player)
            except SQLAlchemyError as e:
                logging.error(e)

    @Base().connection
    @staticmethod
    async def select_all_stuff(session, name_player: str):
        stmt = (
            select(Stuff)
            .join(Inventory, Stuff.invetory_id == Inventory.id)
            .join(Player, Inventory.player_id == Player.id_tg)
            .where(Player.player_name == name_player)
        )
        result = await session.execute(stmt)
        stuff = result.scalars().all()
        if stuff is not None:
            return stuff
        else:
            raise Exception("Такого игрока нет")

