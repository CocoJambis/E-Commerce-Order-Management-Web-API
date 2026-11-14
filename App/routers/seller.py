from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from App.db import get_session
from App.models import ArticoloResponse, ArticoloCreate, User, UserResponse, UserCreate
from App.crud import get_current_seller_user, ArticoloRepository, UserRepository

router = APIRouter(prefix="/seller", tags=["Seller"])


# Registra Seller
@router.post("/register/seller", response_model=UserResponse)
async def create_user_seller(
    new_user: UserCreate, db: AsyncSession = Depends(get_session)
):
    return await UserRepository.create_seller(db=db, new_user=new_user)


# Sell Article
@router.post("/sell", response_model=ArticoloResponse)
async def sell_article(
    articolo: ArticoloCreate,
    current_user: User = Depends(get_current_seller_user),
    db: AsyncSession = Depends(get_session),
):
    return await ArticoloRepository.create_articolo(
        current_user=current_user, db=db, articolo=articolo
    )


# Lista articoli in vendita
@router.get("/articles", response_model=list[ArticoloResponse])
async def get_selled_articles(
    current_user: User = Depends(get_current_seller_user),
    db: AsyncSession = Depends(get_session),
):
    return await ArticoloRepository.get_articles_selled(
        current_user=current_user, db=db
    )
