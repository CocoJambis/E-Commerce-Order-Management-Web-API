from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from App.db import get_session
from App.schemas import ArticoloResponse
import App.crud as crud

router = APIRouter(
    prefix="/articoli",
    tags=["Articoli"]
)

#Lista articoli
@router.get("", response_model=list[ArticoloResponse])
async def lista_articoli(db:AsyncSession = Depends(get_session)):
    return await crud.ArticoloRepository.all_articoli(db)

