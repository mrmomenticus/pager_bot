import logging
from sqlalchemy import ARRAY, Column, ForeignKey, String, Integer, Boolean, Date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pager import configs
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from sqlalchemy.sql.expression import func, select


def created_engine():
    engine = create_async_engine(
        configs.cfg["database"]["type"]
        + "://"
        + configs.cfg["database"]["user"]
        + ":"
        + configs.cfg["database"]["password"]
        + "@"
        + configs.cfg["database"]["host"]
        + ":"
        + configs.cfg["database"]["port"]
        + "/"
        + configs.cfg["database"]["table"],
        echo=configs.cfg["database"]["echo"],
    )

    engine.echo = configs.cfg["database"]["echo"]

    return engine


async def init_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def is_database_exists():
    try:
        # Попытка получить количество строк из таблицы Players
        async with async_session_factory() as session:
            result = await session.execute(select(func.count()).select_from(Player))
            count = result.scalar_one()
            if count == 0:
                logging.info("Таблица Players пустая.")
                return True  # База данных и таблица пустые
            logging.info(f"Таблица Players содержит {count} записей.")
            return False  # База данных и таблица существуют
    except Exception as e:
        logging.error(f"Ошибка при проверке базы данных: {e}")
        return True  # База данных или таблица не существует


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "Players"
    id_tg: Mapped[int] = MappedColumn(primary_key=True)
    inventory: Mapped["Inventory"] = relationship(back_populates="player")
    game_id: Mapped[int] = MappedColumn(ForeignKey("Game.number_group"))
    game: Mapped[list["Game"]] = relationship("Game", back_populates="players")
    username: Mapped[str] = MappedColumn(String(255))
    player_name: Mapped[str] = MappedColumn(String(255))
    is_admin: Mapped[bool] = MappedColumn(Boolean(), default=False)
    photo_state = Column(ARRAY(String), nullable=True) #TODO: в дальнейшем может отдельной таблицей
    
    def clear(self):
        self.id_tg = None
        self.username = None
        self.player_name = None
        self.game_id = None
        self.is_admin = None

class Game(Base):
    __tablename__ = "Game"
    number_group: Mapped[int] = MappedColumn(primary_key=True)
    game_name: Mapped[str] = MappedColumn(String(255))
    date = MappedColumn(Date())
    players: Mapped[list["Player"]] = relationship("Player", back_populates="game")


    def __str__(self):
        return f"{self.date}"
    
class Inventory(Base):
    __tablename__ = "Inventory"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    player_id : Mapped[int] = MappedColumn(Integer, ForeignKey("Players.id_tg"))
    money: Mapped[int] = MappedColumn(Integer)
    
    player: Mapped["Player"] = relationship(back_populates="inventory")
    stuff: Mapped[list["Stuff"]] = relationship(back_populates="inventory")


class Stuff(Base):
    __tablename__ = "Stuff"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    invetory_id: Mapped[int] = MappedColumn(Integer, ForeignKey("Inventory.id"))
    title: Mapped[str] = MappedColumn(String(255))
    price: Mapped[int] = MappedColumn(Integer)
    description: Mapped[str] = MappedColumn(String(255))
    
    inventory: Mapped["Inventory"] = relationship(back_populates="stuff")
    

async_engine = created_engine()

async_session_factory = async_sessionmaker(async_engine)
