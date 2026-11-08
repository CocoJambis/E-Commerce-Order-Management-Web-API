import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from main import app

from App.db import get_session
from App.models import Base, User, Articolo, Order
from App.schemas import (
    UserCreate,
    ArticoloCreate,
    OrderCreate,
    OrderArt
)

from App.crud import (
    UserRepository,
    ArticoloRepository,
    OrderRepository
)



DB_TEST = "sqlite+aiosqlite:///:memory:"




#Costruttore per Tests
class CreateOrderSetup():
    
    @staticmethod
    async def create_user(db:AsyncSession) -> User:
        new_user = UserCreate(
            first_name = "Mario",
            last_name = "Rossi",
            email = "mario.rossi@gmail.com",
            password = "123"
        )
        user = await UserRepository.create_user(
            db = db,
            new_user = new_user
        )

        return user

    @staticmethod
    async def create_user2(db:AsyncSession) -> User:
        new_user = UserCreate(
            first_name= "Mario",
            last_name = "Rossi",
            email = "mario.rossi2@gmail.com",
            password = "123"
        )

        user = await UserRepository.create_user(
            db = db,
            new_user = new_user
        )

        return user

    @staticmethod
    async def create_article(db:AsyncSession) -> Articolo:
        new_article = ArticoloCreate(
            name = "Test",
            desc = "Test",
            prezzo = 10,
            quantità = 20
        )

        articolo = await ArticoloRepository.create_articolo(
            db = db,
            articolo = new_article
        )

        return articolo

    @staticmethod
    async def create_article2(db:AsyncSession):
        new_article = ArticoloCreate(
            name = "Test2",
            desc = "Test2",
            prezzo = 10,
            quantità = 20
        )
        
        articolo = await ArticoloRepository.create_articolo(
            db = db,
            articolo = new_article
        )

        return articolo

    @staticmethod
    async def create_order(db:AsyncSession, user:User, articolo:Articolo) -> Order:

        order_art = OrderArt(
            articolo_id = articolo.id,
            quantità = 1
        )

        new_order = OrderCreate(
            articoli = [
                order_art
            ]
        )

        order = await OrderRepository.create_order(
            db = db,
            ordine = new_order,
            current_user = user
        )

        return order

    @staticmethod
    async def create_order2(db:AsyncSession, user:User, articolo1:Articolo, articolo2:Articolo) -> Order:

        order_art = OrderArt(
            articolo_id = articolo1.id,
            quantità = 1
        )

        order_art2 = OrderArt(
            articolo_id = articolo2.id,
            quantità = 1
        )

        new_order = OrderCreate(
            articoli  = [
                order_art,
                order_art2
            ]
        )

        order = await OrderRepository.create_order(
            db = db,
            ordine = new_order,
            current_user=user
        )

        return order




#Anyio per async
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


#Engine
@pytest.fixture(scope="session")
async def db_engine():

    engine = create_async_engine(DB_TEST, connect_args={"check_same_thread": False})
    yield engine


#Session
@pytest.fixture(scope="function")
async def db_session(db_engine):

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


#Client
@pytest.fixture
async def client(db_session):


    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db


    async with AsyncClient(transport=ASGITransport(app=app), base_url="htttp://test") as ac:

        yield ac

    app.dependency_overrides.clear()