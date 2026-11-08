from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from App.config import settings
import os

DB_URL = settings.db_url or "postgresql+asyncpg://utente_locale:password_locale@localhost:5432/database_locale"

engine = create_async_engine(DB_URL)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session