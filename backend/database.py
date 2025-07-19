from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://wb@localhost:5432/postgres")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session 