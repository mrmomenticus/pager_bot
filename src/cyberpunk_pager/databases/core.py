from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from cyberpunk_pager import configs
from sqlalchemy.orm import Mapped, MappedColumn



def created_database():
    engine = create_async_engine(configs.cfg["database"]["url"], echo=True) # type: ignore
    engine.echo = configs.cfg["database"]["echo"] # type: ignore
    Base.metadata.create_all(engine)
    return engine

class Base(DeclarativeBase):
    pass


class Worker(Base):
    __tablename__ = "workers"
    id: Mapped[int] = MappedColumn(primary_key=True)
    username: Mapped[str] = MappedColumn(String(255))
    
    
async_engine = created_database()

async_session_factory = async_sessionmaker(async_engine)