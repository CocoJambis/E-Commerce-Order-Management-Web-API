from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.db import get_db
from App.schemas import *
import App.crud as crud
from App.models import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

#---------------------ARTICOLI--------------------------

#Crea articolo
@router.post("", response_model=ArticoloResponse)
def crea_articolo(articolo:ArticoloCreate, db:Session = Depends(get_db), current_admin: User = Depends(crud.get_current_admin_user)):
    return crud.create_articolo(db=db, articolo=articolo)

#Modifica prezzo articolo
@router.put("/{articolo_id}", response_model=ArticoloResponse)
def modifica_prezzo_articolo(nuovo_prezzo:ModificaPrezzoArticolo, articolo_id:int, db:Session = Depends(get_db), current_admin: User = Depends(crud.get_current_admin_user)):
    return crud.prezzo_articolo(nuovo_prezzo=nuovo_prezzo, articolo_id=articolo_id, db=db)

#Aggiungi quantità articolo
@router.put("/aggiungigiacenza/{articolo_id}", response_model=ArticoloResponse)
def aggiungi_quantità(nuova_quantità:ModificaGiacenzaArticolo, articolo_id:int, db:Session = Depends(get_db), current_admin: User = Depends(crud.get_current_admin_user)):
    return crud.modifica_giacenza(articolo_id=articolo_id, nuova_giacenza=nuova_quantità, db=db)

#Elimina articolo
@router.delete("/{articolo_id}")
def delete_articolo(articolo_id:int, db:Session = Depends(get_db), current_admin: User = Depends(crud.get_current_admin_user)):
    return crud.delete_articolo(articolo_id=articolo_id, db=db)


#---------------------USERS--------------------------

#Lista tutti gli utenti
@router.get("/users", response_model=list[UserResponse])
def all_users(db:Session = Depends(get_db), current_admin:User = Depends(crud.get_current_admin_user)):
    return crud.user_list(db=db)

#Elimina utente
@router.delete("/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db), current_admin:User = Depends(crud.get_current_admin_user)):
    return crud.delete_user(user_id=user_id, db=db)


#---------------------ORDERS--------------------------

#Tutti gli ordini
@router.get("", response_model=list[OrderResponse])
def all_orders(db:Session = Depends(get_db), current_admin:User = Depends(crud.get_current_admin_user)):
    return crud.all_orders(db=db)

#Lista articoli ordinati in un ordine
@router.get("/articoliordinati/{order_id}", response_model=list[ArticoliOrdinati])
def lista_articoli_ordinati(order_id:int, db:Session = Depends(get_db), current_admin:User = Depends(crud.get_current_admin_user)):
    return crud.lista_articoli_ordinati_by_order_id(order_id=order_id, db=db)

#Elimina ordine
@router.delete("/orders/{order_id}")
def delete_order(order_id:int, db:Session = Depends(get_db), current_admin:User = Depends(crud.get_current_admin_user)):
    return crud.delete_order_admin(order_id=order_id, db=db)
