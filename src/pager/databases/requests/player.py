
from sqlalchemy import select
from pager.databases.models import Player, Base


class PlayerOrm:
    """
    Ищет игрока по его Telegram id.

    Args:
        id_tg: Telegram id

    Returns:
        Player: Возвращает оьъект игрока или None.
    """

    @Base().connection
    @staticmethod
    async def select_player_from_id(session, id_tg: int) -> Player:
        stmt = select(Player).where(Player.id_tg == id_tg)
        result = await session.execute(stmt)
        return result.scalars().first()

    """
        Ищет игрока по его имени.

        Args:
            player_name: Имя игрока

        Returns:
            Player: Возвращает оьъект игрока или None.
    """

    @Base().connection
    @staticmethod
    async def select_player_from_name(session, player_name: str) -> Player:
        stmt = select(Player).where(Player.player_name == player_name)
        result = await session.execute(stmt)
        return result.scalars().first()

    @Base().connection
    @staticmethod
    async def update_new_player(session, new_player: Player):
        async with session.begin():
            session.add(new_player)
            await session.commit()

    @Base().connection
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

    @Base().connection
    @staticmethod
    async def select_photo_state(session, player_name: str):
        stmt = select(Player).where(Player.player_name == player_name)
        result = await session.execute(stmt)
        player = result.scalars().first()
        if player is not None:
            return player.photo_state
        else:
            return None

    @Base().connection
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
