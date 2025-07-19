import asyncio
from models import Base
from database import engine

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_all())
