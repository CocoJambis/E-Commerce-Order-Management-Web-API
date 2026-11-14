from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from App.db import get_session
from App.models import ArticoloResponse
from App.crud import ArticoloRepository

router = APIRouter(prefix="/articoli", tags=["Articoli"])


# Lista articoli
@router.get("", response_model=list[ArticoloResponse])
async def lista_articoli(db: AsyncSession = Depends(get_session)):
    return await ArticoloRepository.all_articoli(db)
