from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from App.config import settings
import os

DATABASE_URL = os.getenv("DATABASE_URL", settings.db_url)

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session