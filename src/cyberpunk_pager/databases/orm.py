
from cyberpunk_pager.databases.core import Worker, async_session_factory

async def insert_data():
    worker = Worker(username="test")
    async with async_session_factory() as session:
        async with session.begin():
            session.add(worker)
            await session.commit()
