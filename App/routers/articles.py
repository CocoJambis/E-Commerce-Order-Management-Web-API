from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from App.db import get_session
from App.models import ArticoloResponse
from App.crud import ArticoloRepository

router = APIRouter(prefix="/articoli", tags=["Articoli"])


# Lista articoli
@router.get("", response_model=list[ArticoloResponse])
async def lista_articoli(db: AsyncSession = Depends(get_session)):
    return await ArticoloRepository.all_articoli(db)


# Cerca articoli by categoria o nome
@router.get("/search", response_model=list[ArticoloResponse])
async def find_articolo(
    category: str | None = Query(None, description="Filtra per categoria scelta"),
    nome: str | None = Query(None, description="Cerca per nome (anche parziale)"),
    db: AsyncSession = Depends(get_session),
):

    return await ArticoloRepository.find_article(db=db, category=category, nome=nome)
