from sqlalchemy import String, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from cyberpunk_pager import configs
from sqlalchemy.orm import Mapped, MappedColumn

meta = MetaData()

def created_engine():
    engine = create_async_engine(configs.cfg["database"]["url"], echo=True) # type: ignore
    engine.echo = configs.cfg["database"]["echo"] # type: ignore
    
    
    return engine

async def init_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
class Base(DeclarativeBase):
    pass


class Worker(Base):
    __tablename__ = "workers"
    id: Mapped[int] = MappedColumn(primary_key=True)
    username: Mapped[str] = MappedColumn(String(255))
    
    
async_engine = created_engine()

async_session_factory = async_sessionmaker(async_engine)
