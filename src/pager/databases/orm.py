import logging
from sqlalchemy import func, select
from pager.databases.core import Game, Player, async_session_factory


"""
    ORM для работы с таблицей Players.
"""


class PlayerOrm:
    """
    Ищет игрока по его Telegram id.

    Args:
        id_tg: Telegram id

    Returns:
        Player: Возвращает оьъект игрока или None.
    """

    @staticmethod
    async def select_player_from_id(id_tg: int) -> Player:
        stmt = select(Player).where(Player.id_tg == id_tg)
        async with async_session_factory() as session:
            result = await session.execute(stmt)
            return result.scalars().first()

    """
        Ищет игрока по его имени.

        Args:
            player_name: Имя игрока

        Returns:
            Player: Возвращает оьъект игрока или None.
    """

    @staticmethod
    async def select_player_from_name(player_name: str) -> Player:
        stmt = select(Player).where(Player.player_name == player_name)
        async with async_session_factory() as session:
            result = await session.execute(stmt)
            return result.scalars().first()

    """
        Ищет игрока по его Telegram id.
        
        Args:
            id_tg: Telegram id
            
        Returns:
            Game: Возвращает все игры где присутствует этот игрок или None.
    """

    @staticmethod
    async def select_games_by_player_id(id_tg: int):
        stmt = (
            select(Game)
            .join(Player, Game.player_id == Player.id_tg)
            .where(Player.id_tg == id_tg)
        )
        async with async_session_factory() as session:
            result = await session.execute(stmt)
            games = result.scalars().all()
            return games

    @staticmethod
    async def update_new_player(new_player: Player):
        async with async_session_factory() as session:
            async with session.begin():
                session.add(new_player)
                await session.commit()

    """
        Добавляет url фото в photo_state игрока.
        
        Args:
            player_name: Имя игрока.
            photo_url: url фото.
    """

    @staticmethod
    async def create_photo_state(player_name: str, photo_url: str):  # TODO: узкое место
        async with async_session_factory() as session:
            async with session.begin():
                stmt = select(Player).where(
                    Player.player_name == player_name
                )  # TODO: Добавить исключение если не найден игрок
                result = await session.execute(stmt)
                player = result.scalars().first()
                if player is None:
                    logging.error("Такого игрока нет")
                    raise Exception("Такого игрока нет")
                player.photo_state = (
                    player.photo_state or []
                )  # Initialize as empty list if None
                player.photo_state = player.photo_state + [photo_url]
                await session.commit()

    @staticmethod
    async def select_photo_state(
        player_name: str,
    ):  # TODO: может быть ошибка, если в базе есть 2 одинаковых игрока по имени
        async with async_session_factory() as session:
            stmt = select(Player).where(Player.player_name == player_name)
            result = await session.execute(stmt)
            player = result.scalars().all()
            if player is not None:
                return player
            else:
                return None

    @staticmethod
    async def delete_photo_state(player_name: str):
        async with async_session_factory() as session:
            async with session.begin():
                stmt = select(Player).where(Player.player_name == player_name)
                result = await session.execute(stmt)
                player = result.scalars().first()
                if player is not None:
                    player.photo_state = None
                    await session.commit()
                else:
                    logging.error("Такого игрока нет")
                    raise Exception("Такого игрока нет")


class GameOrm:
    @staticmethod
    async def get_game_by_number_group(number_group: int) -> Game:
        stmt = select(Game).where(Game.number_group == number_group)
        async with async_session_factory() as session:
            result = await session.execute(stmt)
            result = result.scalars().first()
            if result is not None:
                return result
            else:
                return None

    @staticmethod
    async def set_date_game(number_group: int, date_str: str):
        async with async_session_factory() as session:
            async with session.begin():
                stmt = select(Game).where(Game.number_group == number_group)
                result = await session.execute(stmt)
                game = result.scalars().first()
                game.date = func.to_date(date_str, "DD.MM.YYYY")
                await session.commit()

    @staticmethod
    async def set_new_game(new_game: Game):
        async with async_session_factory() as session:
            async with session.begin():
                session.add(new_game)
                await session.commit()
