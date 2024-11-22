import logging
from sqlalchemy import select
from pager.databases.models import Inventory, Player, Stuff
from sqlalchemy.exc import SQLAlchemyError

from pager.databases.requests.base import BaseRequest
from pager.utils.exeption import NotFoundError


class StuffRequest(BaseRequest[Stuff]): 
    @staticmethod
    @BaseRequest.connection
    async def add_new_stuff(
        session, name_player: str, name_item: str, price_item: int, description: str
    ):
        stmt = (
            select(Stuff)
            .join(Inventory)
            .join(Player)
            .where(Player.player_name == name_player)
            .where(Stuff.title == name_item)
        )
        result = await session.execute(stmt)
        stuff = result.scalars().first()
        if stuff is not None:
            raise ValueError("Такой предмет уже есть у данного игрока")
        else:
            stmt = (
                select(Inventory)
                .join(Player, Inventory.player_id == Player.id_tg)
                .where(Player.player_name == name_player)
            )
            result = await session.execute(stmt)
            inventory = result.scalars().first()
            if inventory is not None:
                session.add(
                    Stuff(
                        invetory_id=inventory.id,
                        title=name_item,
                        price=price_item,
                        description=description,
                    )
                )
                await session.commit()
            else:
                raise SQLAlchemyError("Такого игрока нет")

    @BaseRequest.connection
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
                    logging.warning(f"Такого предмета нет: {name_item}")
                    raise NotFoundError(name_item, name_player)
            except SQLAlchemyError as e:
                logging.error(e)

    @BaseRequest.connection
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
