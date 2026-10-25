from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from App.config import settings

engine = create_async_engine(settings.db_url)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session