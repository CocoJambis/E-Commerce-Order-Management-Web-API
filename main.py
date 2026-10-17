from fastapi import FastAPI
import uvicorn
from App.config import settings
from App.routers import users, orders, articles


app = FastAPI(
    title="E-Commerce Order Management API",
    description="API enterprise per la gestione di utenti, prodotti e ordini con transazioni atomiche.",
    version=settings.version
)


@app.get("/", tags=["Root"])
def home():
    return {"message" : "Welcome to the E-Commerce API!"}

#Routers
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(orders.router)

if __name__ == "__main__":
    uvicorn.run(app, port=settings.port)