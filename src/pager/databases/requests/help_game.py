import logging

from sqlalchemy import select
from pager.databases.models import HelpGame
from pager.databases.requests.base import BaseRequest
from sqlalchemy.exc import SQLAlchemyError
from pager.utils.globals import number_group

class HelpGameRequest(BaseRequest):
    @BaseRequest.connection
    @staticmethod
    async def add_help(session, path: str):
        try:
            
            help_game_model = HelpGame(game_id=number_group, path=path)
        
            session.add(help_game_model)
            await session.commit()
        except Exception as e:
            logging.error(e)
            session.rollback()
            raise e
        
        
    @BaseRequest.connection
    @staticmethod
    async def get_help(session, group: int):
        try:
            stmt = select(HelpGame).where(HelpGame.game_id == number_group)
            result = await session.execute(stmt)
            help = result.scalars().all()
        except SQLAlchemyError as e:
            logging.error(e)
            raise e
        return help
        
