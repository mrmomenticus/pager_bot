import logging
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pager import configs
from sqlalchemy.sql.expression import func, select

from pager.databases.models import Player

class Core():
    def __init__(self):
        self.engine = self.create_engine()
        self.init_database()
        self.is_database_exists()
        self.session = async_sessionmaker(self.engine)

    @staticmethod
    def create_engine() -> Engine:
        return create_async_engine(
            url=f"{configs.cfg['database']['type']}://"
            f"{configs.cfg['database']['user']}:"
            f"{configs.cfg['database']['password']}@"
            f"{configs.cfg['database']['host']}:"
            f"{configs.cfg['database']['port']}/"
            f"{configs.cfg['database']['table']}",
            echo=configs.cfg["database"]["echo"],
        )

    async def init_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)

    async def is_database_exists(self) -> bool:
        try:
            async with self.session() as session:
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
        
    def connection(func):
        async def wrapper(*args, **kwargs):
            async with Core().session() as session:
                return await func(session, *args, **kwargs)

            return wrapper
