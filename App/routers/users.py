from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from App.db import get_session

from App.models import UserResponse, UserCreate, Token, OrderResponse, ArticoliOrdinati

from App.crud import (
    UserRepository,
    get_current_active_user,
    login_for_access_token,
    OrderRepository,
)
from App.auth import OAuth2PasswordRequestForm
from App.models import User

router = APIRouter(prefix="/users", tags=["Users"])


# Registra Utente
@router.post("/register", response_model=UserResponse)
async def create_user(new_user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await UserRepository.create_user(db=db, new_user=new_user)


# Token
@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    return await login_for_access_token(form_data=form_data, db=db)


# Ordini Utente
@router.get("/orders", response_model=list[OrderResponse])
async def lista_orders_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
):
    return await OrderRepository.get_user_orders(user_id=current_user.id, db=db)


# Dettagli ordine
@router.get("/orders/details/{order_id}", response_model=list[ArticoliOrdinati])
async def dettagli_ordine(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
):
    return await OrderRepository.dettagli_ordine(
        current_user=current_user, order_id=order_id, db=db
    )
