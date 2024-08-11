import logging
from sqlalchemy import String, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pager import configs
from sqlalchemy.orm import Mapped, MappedColumn
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
        + "/",
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
            result = await session.execute(select(func.count()).select_from(Players))
            count = result.scalar_one()
            if(count == 0):
                logging.info("Таблица Players пустая.")
                return True  # База данных и таблица пустые
            logging.info(f"Таблица Players содержит {count} записей.")
            return False  # База данных и таблица существуют
    except Exception as e:
        logging.error(f"Ошибка при проверке базы данных: {e}")
        return True  # База данных или таблица не существует 

class Base(DeclarativeBase):
    pass


class Players(Base):
    __tablename__ = "Players"
    id_tg: Mapped[int] = MappedColumn(primary_key=True)
    username: Mapped[str] = MappedColumn(String(255))
    player_name: Mapped[str] = MappedColumn(String(255))
    number_group: Mapped[str] = MappedColumn(Integer)
    
    # def clear(self):
    #     self.id_tg = None
    #     self.username = None
    #     self.player_name = None
    #     self.number_group = None
        
    


async_engine = created_engine()

async_session_factory = async_sessionmaker(async_engine)


    
