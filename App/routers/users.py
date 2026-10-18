from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.db import get_db
from App.schemas import *
import App.crud as crud
from App.auth import *
from App.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#Registra Utente
@router.post("", response_model=UserResponse)
def create_user(new_user:UserCreate, db:Session = Depends(get_db)):
    return crud.create_user(db=db, new_user=new_user)

#Token
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    return crud.login_for_access_token(form_data=form_data, db=db)

#Ordini Utente
@router.get("/orders", response_model=list[OrderResponse])
def lista_orders_user(current_user:User = Depends(crud.get_current_active_user), db:Session = Depends(get_db)):
    return crud.get_user_orders(user_id=current_user.id, db=db)

#Dettagli ordine
@router.get("/orders/details", response_model=list[ArticoliOrdinati])
def dettagli_ordine(current_user:User = Depends(crud.get_current_active_user), db:Session = Depends(get_db)):

    ordini_utente = current_user.orders

    if not ordini_utente:
        return []

    dettagli = [dettaglio for ord in ordini_utente for dettaglio in ord.dettagli_articoli]

    return dettagli