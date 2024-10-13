from sqlalchemy import func, select
from pager.databases.models import Game, Player, Base


class GameOrm:
    @Base().connection
    @staticmethod
    async def get_game_by_number_group(session, number_group: int) -> Game:
        stmt = select(Game).where(Game.number_group == number_group)
        result = await session.execute(stmt)
        result = result.scalars().first()
        if result is not None:
            return result
        else:
            return None

    @Base().connection
    @staticmethod
    async def set_date_game(session, number_group: int, date_str: str):
        async with session.begin():
            stmt = select(Game).where(Game.number_group == number_group)
            result = await session.execute(stmt)
            game = result.scalars().first()
            game.date = func.to_date(date_str, "DD.MM.YYYY")
            await session.commit()

    @Base().connection
    @staticmethod
    async def set_new_game(session, new_game: Game):
        async with session.begin():
            session.add(new_game)
            await session.commit()
            
            
    @Base().connection
    @staticmethod
    async def get_players_from_game(session, number_group: int):
        stmt = select(Player).join(Game).where(Game.number_group == number_group)
        result = await session.execute(stmt)
        return result.scalars().all()
        
