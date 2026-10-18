from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.db import get_db
from App.schemas import *
import App.crud as crud
from App.models import User


router = APIRouter(
    prefix="/articoli",
    tags=["Articoli"]
)

#Lista articoli
@router.get("", response_model=list[ArticoloResponse])
def lista_articoli(db:Session = Depends(get_db)):
    return crud.all_articoli(db)

