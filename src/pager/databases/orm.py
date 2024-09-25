import logging
from sqlalchemy import func, select
from pager.databases.core import Game, Player, Inventory, Stuff, async_session_factory
from pager.exeption import NotFoundError
from sqlalchemy.exc import SQLAlchemyError


"""
    ORM для работы с таблицей Players.
"""


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            return await func(session, *args, **kwargs)

    return wrapper


class PlayerOrm:
    """
    Ищет игрока по его Telegram id.

    Args:
        id_tg: Telegram id

    Returns:
        Player: Возвращает оьъект игрока или None.
    """

    @connection
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

    @connection
    @staticmethod
    async def select_player_from_name(session, player_name: str) -> Player:
        stmt = select(Player).where(Player.player_name == player_name)
        result = await session.execute(stmt)
        return result.scalars().first()

    """
        Ищет игрока по его Telegram id.
        
        Args:
            id_tg: Telegram id
            
        Returns:
            Game: Возвращает все игры где присутствует этот игрок или None.
    """

    @connection
    @staticmethod
    async def select_games_by_player_id(session, id_tg: int):
        stmt = (
            select(Game)
            .join(Player, Game.player_id == Player.id_tg)
            .where(Player.id_tg == id_tg)
        )
        result = await session.execute(stmt)
        games = result.scalars().all()
        return games

    @connection
    @staticmethod
    async def update_new_player(session, new_player: Player):
        async with session.begin():
            session.add(new_player)
            session.add(Inventory(player_id=new_player.id_tg))
            await session.commit()

    """
        Добавляет url фото в photo_state игрока.
        
        Args:
            player_name: Имя игрока.
            photo_url: url фото.
    """

    @connection
    @staticmethod
    async def create_photo_state(
        session, player_name: str, photo_url: str
    ):  # TODO: узкое место
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

    @connection
    @staticmethod
    async def select_photo_state(
        session,
        player_name: str,
    ):  # TODO: может быть ошибка, если в базе есть 2 одинаковых игрока по имени
        stmt = select(Player).where(Player.player_name == player_name)
        result = await session.execute(stmt)
        player = result.scalars().all()
        if player is not None:
            return player
        else:
            return None

    @connection
    @staticmethod
    async def delete_photo_state(session, player_name: str):
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

    @connection
    @staticmethod
    async def update_money(session, player_name: str, money: int):
        async with session.begin():
            stmt = (
                select(Inventory)
                .join(Player, Inventory.player_id == Player.id_tg)
                .where(Player.player_name == player_name)
            )
            result = await session.execute(stmt)
            inventory = result.scalars().first()
            if inventory is not None:
                sum = inventory.money + money
                inventory.money += money
                await session.commit()
                return sum
            else:
                logging.debug("Такого игрока нет")
                return None

    @connection
    @staticmethod
    async def take_money(session, player_name: str, money: int):
        async with session.begin():
            stmt = (
                select(Inventory)
                .join(Player, Inventory.player_id == Player.id_tg)
                .where(Player.player_name == player_name)
            )
            result = await session.execute(stmt)
            inventory = result.scalars().first()
            if inventory is not None:
                sum = inventory.money - money
                inventory.money -= money
                await session.commit()
                return sum
            else:
                logging.debug("Такого игрока нет")
                return None

    @connection
    @staticmethod
    async def select_money(session, player_name: str):
        stmt = (
            select(Inventory)
            .join(Player, Inventory.player_id == Player.id_tg)
            .where(Player.player_name == player_name)
        )
        result = await session.execute(stmt)
        inventory = result.scalars().first()
        if inventory is not None:
            return inventory.money
        else:
            return None

    @connection
    @staticmethod
    async def add_new_stuff(
        session, player_name: str, item_name: str, price_item: int, description: str
    ):
        stuff = await session.scalars(
            select(Stuff).join(Inventory).join(Player).where(Player.player_name == player_name).where(Stuff.title == item_name)
        )
        if stuff.first() is not None:
            logging.warning("Такой предмет уже есть у данного игрока")
            raise ValueError("Такой предмет уже есть у данного игрока")
        else:
            async with session.begin():
            
                stmt = (    
                    select(Inventory)
                    .join(Player, Inventory.player_id == Player.id_tg)
                    .where(Player.player_name == player_name)
                )
                result = await session.execute(stmt)
                inventory = result.scalars().first()
                if inventory is not None:
                    session.add(
                        Stuff(
                            invetory_id=inventory.id,
                            title=item_name,
                            price=price_item,
                            description=description,
                        )
                    )
                else:
                    logging.warning(f"Такого игрока нет {player_name}")
                    raise SQLAlchemyError("Такого игрока нет")
                await session.commit()

    @connection
    @staticmethod
    async def delete_stuff(session, name_player: str, name_item: str):
        async with session.begin():
            try:
                stmt = (
                    select(Stuff)
                    .join(Inventory, Stuff.invetory_id == Inventory.id)
                    .join(Player, Inventory.player_id == Player.id_tg)
                    .where(Player.player_name == name_player, Stuff.title == name_item)
                )
                result = await session.execute(stmt)
                stuff = result.scalars().first()
                if stuff is not None:
                    await session.delete(stuff)
                else:
                    raise NotFoundError(Stuff.__tablename__, name_item, name_player)
            except SQLAlchemyError as e:
                logging.error(e)
    
    @connection
    @staticmethod
    async def select_all_stuff(session, name_player: str):
        stmt = (
            select(Stuff)
            .join(Inventory, Stuff.invetory_id == Inventory.id)
            .join(Player, Inventory.player_id == Player.id_tg)
            .where(Player.player_name == name_player)
        )
        result = await session.execute(stmt)
        stuff = result.scalars().all()
        logging.debug(f"Type of stuff: {type(stuff)}")
        if stuff is not None:
            return stuff
        else: 
            return None
        


class GameOrm:
    @connection
    @staticmethod
    async def get_game_by_number_group(session, number_group: int) -> Game:
        stmt = select(Game).where(Game.number_group == number_group)
        result = await session.execute(stmt)
        result = result.scalars().first()
        if result is not None:
            return result
        else:
            return None

    @connection
    @staticmethod
    async def set_date_game(session, number_group: int, date_str: str):
        async with session.begin():
            stmt = select(Game).where(Game.number_group == number_group)
            result = await session.execute(stmt)
            game = result.scalars().first()
            game.date = func.to_date(date_str, "DD.MM.YYYY")
            await session.commit()

    @connection
    @staticmethod
    async def set_new_game(session, new_game: Game):
        async with session.begin():
            session.add(new_game)
            await session.commit()
