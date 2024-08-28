from sqlalchemy import func, select
from pager.databases.core import Game, Players, async_session_factory


async def get_player_from_id(id_tg : int) -> Players:
    stmt = select(Players).where(Players.id_tg == id_tg)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        return result.scalars().first()

async def get_game_by_number_group(number_group : int) -> Game:
    stmt = select(Game).where(Game.number_group == number_group)
    async with async_session_factory() as session:
        result = await session.execute(stmt)
        result = result.scalars().first()
        if result is not None:
            return result
        else:
            return None
    
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
        games = result.scalars().first()
        
        return games
    
async def set_new_player(new_player : Players):
    async with async_session_factory() as session:
        async with session.begin():
            session.add(new_player)
            await session.commit()
            
async def set_date_game(number_group: int, date_str: str):
    async with async_session_factory() as session:
        async with session.begin():
            stmt = select(Game).where(Game.number_group == number_group)
            result = await session.execute(stmt)
            game = result.scalars().first()
            game.date = func.to_date(date_str, 'DD.MM.YYYY')
            await session.commit()
            
            
async def set_new_game(new_game : Game):
    async with async_session_factory() as session:
        async with session.begin():
            session.add(new_game)
            await session.commit()
            
async def set_new_photo_state(id_tg: int, photo_url: str): #TODO: узкое место 
    async with async_session_factory() as session:
        async with session.begin():
            stmt = select(Players).where(Players.id_tg == id_tg)
            result = await session.execute(stmt)
            player = result.scalars().first()
            player.photo_state = player.photo_state + [photo_url]
            await session.commit()
            
