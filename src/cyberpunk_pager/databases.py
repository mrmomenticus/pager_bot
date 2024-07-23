import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from cyberpunk_pager import configs

engine = create_async_engine(configs.cfg["url_database"], echo=True # type: ignore
)


async def get_versio():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT version()"))
        print(f"Server version: {res}")


asyncio.run(get_versio())
