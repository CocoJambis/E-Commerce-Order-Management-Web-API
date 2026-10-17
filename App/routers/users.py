from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.db import get_db
from App.schemas import *
import App.crud as crud


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#Crea utente
@router.post("", response_model=UserResponse)
def create_user(new_user:UserCreate, db:Session = Depends(get_db)):
    return crud.create_user(db=db, new_user=new_user)

#Lista tutti gli utenti
@router.get("", response_model=list[UserResponse])
def all_users(db:Session = Depends(get_db)):
    return crud.user_list(db=db)

#Elimina utente
@router.delete("/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    return crud.delete_user(user_id=user_id, db=db)
    
#Lista ordini utente
@router.get("/{user_id}/orders", response_model=list[OrderResponse])
def lista_orders_user(user_id:int, db:Session = Depends(get_db)):
    return crud.get_user_orders(user_id=user_id, db=db)
    