from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.db import get_db
from App.schemas import *
import App.crud as crud


router = APIRouter(
    prefix="/articoli",
    tags=["Articoli"]
)

#Crea articolo
@router.post("", response_model=ArticoloResponse)
def crea_articolo(articolo:ArticoloCreate, db:Session = Depends(get_db)):
    return crud.create_articolo(db=db, articolo=articolo)

#Lista articoli
@router.get("", response_model=list[ArticoloResponse])
def lista_articoli(db:Session = Depends(get_db)):
    return crud.all_articoli(db)

#Modifica prezzo articolo
@router.put("/{articolo_id}", response_model=ArticoloResponse)
def modifica_prezzo_articolo(nuovo_prezzo:ModificaPrezzoArticolo, articolo_id:int, db:Session = Depends(get_db)):
    return crud.prezzo_articolo(nuovo_prezzo=nuovo_prezzo, articolo_id=articolo_id, db=db)

#Aggiungi quantità articolo
@router.put("/aggiungigiacenza/{articolo_id}", response_model=ArticoloResponse)
def aggiungi_quantità(nuova_quantità:ModificaGiacenzaArticolo, articolo_id:int, db:Session = Depends(get_db)):
    return crud.modifica_giacenza(articolo_id=articolo_id, nuova_giacenza=nuova_quantità, db=db)

#Elimina articolo
@router.delete("/{articolo_id}")
def delete_articolo(articolo_id:int, db:Session = Depends(get_db)):
    return crud.delete_articolo(articolo_id=articolo_id, db=db)