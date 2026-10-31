from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from App.config import settings
from App.routers import users, orders, articles, admin
from App.models import Base
from App.db import engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    # --- Avvio: Crea le tabelle se non esistono ---
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # --- Spegnimento: (Vuoto) ---


app = FastAPI(
    title="E-Commerce Order Management API",
    description="API enterprise per la gestione di utenti, prodotti e ordini con transazioni atomiche.",
    version=settings.version,
    lifespan=lifespan
)


@app.get("/", tags=["Root"])
async def home():
    return {"message" : "Welcome to the E-Commerce API!"}

#Routers
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(orders.router)
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)