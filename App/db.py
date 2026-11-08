from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from App.config import settings
import os

DB_URL = os.getenv(settings.db_url, "postgresql+asyncpg://utente_docker:password_docker_sicura@db:5432/database_docker")

engine = create_async_engine(DB_URL)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session