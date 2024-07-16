
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config.config import cfg

engine = create_async_engine(cfg["url_database"], echo=True)
async def test():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(res.all())

