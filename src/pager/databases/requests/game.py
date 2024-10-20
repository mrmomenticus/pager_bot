import logging
from sqlalchemy import func, select
from pager.databases.models import Game, Player
from pager.databases.requests.base import BaseDAO
from sqlalchemy.exc import SQLAlchemyError

from pager.exeption.exeption import NotFoundError


class GameRequest(BaseDAO[Game]):
    @BaseDAO.connection
    @staticmethod
    async def get_game_by_number_group(session, number_group: int) -> Game:
        try:
            stmt = select(Game).where(Game.number_group == number_group)
            result = await session.execute(stmt)
            result = result.scalars().first()
        except SQLAlchemyError as e:
            logging.error(e)
            raise e
        if result is not None:
            return result
        else:
            raise NotFoundError(number_group)

    @BaseDAO.connection
    @staticmethod
    async def set_date_game(session, number_group: int, date_str: str):
        async with session.begin():
            try:
                stmt = select(Game).where(Game.number_group == number_group)
                result = await session.execute(stmt)
                game = result.scalars().first()
                if game is None:
                    raise NotFoundError(number_group, date_str)
                game.date = func.to_date(date_str, "DD.MM.YYYY")
                await session.commit()
            except SQLAlchemyError as e:
                logging.error(e + f"number_group: {number_group}, date_str: {date_str}")
                session.rollback()
                raise e

    @BaseDAO.connection
    @staticmethod
    async def set_new_game(session, new_game: Game):
        async with session.begin():
            session.add(new_game)
            await session.commit()

    @BaseDAO.connection
    @staticmethod
    async def get_players_from_game(session, number_group: int):
        stmt = select(Player).join(Game).where(Game.number_group == number_group)
        result = await session.execute(stmt)
        return result.scalars().all()
