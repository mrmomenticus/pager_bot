from sqlalchemy import select
from pager.databases.core import Game, Players, async_session_factory


# async def insert_data():
#     await init_database()
#     Players = Players( id=1, username="test", player_name="test", number_group=1)
#     async with async_session_factory() as session:
#         async with session.begin():
#             session.add(Players)
#             await session.commit()

async def get_player_from_id(id_tg : int) -> Players:
    stmt = select(Players).where(Players.id_tg == id_tg)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().first()
    
async def get_games_by_player_id(id_tg: int):
    # Создаем запрос для получения всех игр, связанных с определенным id_tg
    stmt = (
        select(Game)
        .join(Players, Game.number_group == Players.game_id)
        .where(Players.id_tg == id_tg)
    )
    
    # Выполняем запрос
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        
        # Получаем список игр
        games = result.scalars().all()
        
        return games
    
async def set_new_player(new_player : Players):
    async with async_session_factory() as session:
        async with session.begin():
            session.add(new_player)
            await session.commit()