
import logging
import typing
from sqlalchemy import Engine, func, select
from pager.databases.models import BaseModel, Player
from pager.utils import configs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import SQLAlchemyError


T = typing.TypeVar("T", bound=BaseModel) 

class BaseDAO(typing.Generic[T]):
    _session = None
    _engine = None
    model: type[T]
    
    @classmethod
    def session(cls):
        if cls._session is None:
            cls._session = async_sessionmaker(cls.create_engine(), class_=AsyncSession)()
        return cls._session
    
    @classmethod
    def engine(cls):
        if cls._engine is None:
            cls._engine = cls.create_engine()
        return cls._engine
    
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
    
    @staticmethod #TODO: переделать
    def connection(func):
        async def wrapper(*args, **kwargs):
            async with BaseDAO.session() as session:
                return await func(session, *args, **kwargs)
        return wrapper
    
    @classmethod
    async def is_database_exists(cls) -> bool:
        try:
            async with cls.session() as session:
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
        
    
    @classmethod
    async def init_database(cls):
        async with cls.engine().begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
            
    @classmethod
    async def add(cls, session: AsyncSession, **values: dict[str, typing.Any]) -> T:
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: list[dict[str, typing.Any]]) -> list[T]:
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        return new_instances
    
