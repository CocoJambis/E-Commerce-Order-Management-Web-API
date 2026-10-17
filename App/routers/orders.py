from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.schemas import *
from App.db import get_db
import App.crud as crud

router = APIRouter(
    prefix="/ordini",
    tags=["Ordini"]
)

#Crea ordine
@router.post("", response_model=OrderResponse)
def add_order(order:OrderCreate, db:Session = Depends(get_db)):
    return crud.create_order(db=db, ordine=order)

#Tutti gli ordini
@router.get("", response_model=list[OrderResponse])
def all_orders(db:Session = Depends(get_db)):
    return crud.all_orders(db=db)

#Lista articoli ordinati in un ordine
@router.get("/articoliordinati/{order_id}", response_model=list[ArticoliOrdinati])
def lista_articoli_ordinati(order_id:int, db:Session = Depends(get_db)):
    return crud.lista_articoli_ordinati_by_order_id(order_id=order_id, db=db)

#Modifica quantità articolo ordinata
@router.put("ordinearticolo/{ordine_id}", response_model=ArticoliOrdinati)
def modifica_quantità_articolo_ordinata(ordine_id:int, nuova_quantità:OrderArt, db:Session = Depends(get_db)):
    return crud.edit_order(nuova_quantità=nuova_quantità, order_id=ordine_id, db=db)

#Elimina ordine
@router.delete("/{ordine_id}")
def delete_order(ordine_id:int, db:Session = Depends(get_db)):
    return crud.delete_order(order_id=ordine_id, db=db)

#Rimuovi un articolo dall'ordine    
@router.delete("/articolo/{ordine_id}/{articolo_id}")
def delete_articolo_order(ordine_id:int, articolo_id:int, db:Session = Depends(get_db)):
    return crud.delete_order_articolo(order_id=ordine_id, articolo_id=articolo_id, db=db)