import logging
from sqlalchemy import select
from pager.databases.models import Mission
from pager.databases.requests.base import BaseRequest
from sqlalchemy.exc import SQLAlchemyError
from pager.utils.globals import number_group


class MissionRequest(BaseRequest):
    @BaseRequest.connection
    @staticmethod
    async def add_mission(session, mission: dict):
        try:
            mission_model = Mission(
                game_id=number_group,
                local=mission["local"],
                desctription=mission["description"],
                reward=mission["reward"],
            )
            session.add(mission_model)
            await session.commit()
        except Exception as e:
            logging.error(e)
            session.rollback()
            raise e

    @BaseRequest.connection
    @staticmethod
    async def get_missions(session, group: int):
        try:
            stmt = select(Mission).where(Mission.game_id == number_group)
            result = await session.execute(stmt)
            missions = result.scalars().all()
        except SQLAlchemyError as e:
            logging.error(e)
            raise e
        return missions
