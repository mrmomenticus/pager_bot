
import logging
from sqlalchemy import select
from pager.databases.models import Player
from pager.databases.requests.base import BaseRequest
from sqlalchemy.exc import SQLAlchemyError

from pager.exeption.exeption import NotFoundError


class PlayerRequest(BaseRequest[Player]):
    
    @BaseRequest.connection
    @staticmethod
    async def select_player(session, data: str | int) -> Player:
        """
        Ищет игрока по его ID Telegram или имени.

        :param session: сессия sqlalchemy
        :param data: ID Telegram или имя игрока
        :return: объект Player, или None если игрока не существует
        """
        try:
            if isinstance(data, int):
                stmt = select(Player).where(Player.id_tg == data)
            else:
                stmt = select(Player).where(Player.player_name == data)
            result = await session.execute(stmt)
            player = result.scalars().first()
            if player is None:
                logging.warning(f"Такого игрока нет: {data}")
                raise NotFoundError(data)
            return player
        except SQLAlchemyError as e:
            logging.error(e)
            raise e


    @BaseRequest.connection #TODO: заменить на метод из BaseDAO
    @staticmethod
    async def update_new_player(session, new_player: Player):
        try:
            async with session.begin():
                session.add(new_player)
                await session.commit()
        except SQLAlchemyError as e:
            logging.error(e)
            session.rollback()
            raise e
            

    @BaseRequest.connection
    @staticmethod
    async def create_photo_state(session, player_name: str, photo_url: str):
        async with session.begin():
            stmt = select(Player).where(Player.player_name == player_name)
            result = await session.execute(stmt)
            player = result.scalars().first()
            if player is None:
                raise Exception("Такого игрока нет")
            player.photo_state = (
                player.photo_state or []
            )  # Initialize as empty list if None
            player.photo_state = player.photo_state + [photo_url]
            await session.commit()

    @BaseRequest.connection
    @staticmethod
    async def select_photo_state(session, player_name: str):
        stmt = select(Player).where(Player.player_name == player_name)
        result = await session.execute(stmt)
        player = result.scalars().first()
        if player is not None:
            return player.photo_state
        else:
            return None

    @BaseRequest.connection
    @staticmethod
    async def delete_photo_state(session, player_name: str):
        async with session.begin():
            stmt = select(Player).where(Player.player_name == player_name)
            result = await session.execute(stmt)
            player = result.scalars().first()
            if player is not None:
                player.photo_state = []
                await session.commit()
            else:
                raise Exception("Такого игрока нет")
            
            
    @BaseRequest.connection
    @staticmethod
    async def select_all_admins(session):
        stmt = select(Player).where(Player.is_admin.is_(True)) 
        result = await session.execute(stmt)
        return result.scalars().all()
