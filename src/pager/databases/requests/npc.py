import logging

from sqlalchemy import select
from pager.databases.models import Npc
from pager.databases.requests.base import BaseRequest
from sqlalchemy.exc import SQLAlchemyError

class NpcRequest(BaseRequest):
    @BaseRequest.connection
    @staticmethod
    async def add_npc(session, npc: dict):
        try:
            npc_model = Npc(
                game_id=int(npc["number_group"]),
                name=npc["name"],
                local=npc["local"],
                description=npc["description"],
            )
        
            session.add(npc_model)
            await session.commit()
        except Exception as e:
            logging.error(e)
            session.rollback()
            raise e
        
        
    @BaseRequest.connection
    @staticmethod
    async def get_npcs(session, number_group: int):
        try:
            stmt = select(Npc).where(Npc.game_id == number_group)
            result = await session.execute(stmt)
            npcs = result.scalars().all()
        except SQLAlchemyError as e:
            logging.error(e)
            raise e
        return npcs
        
