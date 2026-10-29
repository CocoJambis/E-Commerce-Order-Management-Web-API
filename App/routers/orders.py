from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from App.schemas import (OrderResponse,
                         OrderCreate,
                         OrderArt,
                         ArticoliOrdinati)
from App.db import get_session
import App.crud as crud
from App.models import User

router = APIRouter(
    prefix="/ordini",
    tags=["Ordini"]
)

#Crea ordine
@router.post("", response_model=OrderResponse)
async def add_order(order:OrderCreate, db:AsyncSession = Depends(get_session), current_user:User = Depends(crud.get_current_active_user)):
    return await crud.OrderRepository.create_order(db=db, 
                             ordine=order, 
                             current_user=current_user)

#Modifica quantità articolo ordinata
@router.put("ordinearticolo/{ordine_id}", response_model=ArticoliOrdinati)
async def modifica_quantità_articolo_ordinata(ordine_id:int, nuova_quantità:OrderArt, 
                                              db:AsyncSession = Depends(get_session), 
                                              current_user:User = Depends(crud.get_current_active_user)):
    
    
    return await crud.OrderRepository.edit_order(current_user=current_user, 
                           nuova_quantità=nuova_quantità, 
                           order_id=ordine_id, 
                           db=db)

#Rimuovi un articolo dall'ordine    
@router.delete("/articolo/{ordine_id}/{articolo_id}")
async def delete_articolo_order(ordine_id:int, articolo_id:int, 
                                db:AsyncSession = Depends(get_session), 
                                current_user:User = Depends(crud.get_current_active_user)):

    
    return await crud.OrderRepository.delete_order_articolo(current_user=current_user,
                                      order_id=ordine_id, 
                                      articolo_id=articolo_id, 
                                      db=db)

#Rimuovi ordine
@router.delete("/delete/{ordine_id}")
async def delete_order(ordine_id:int, db:AsyncSession = Depends(get_session), current_user:User = Depends(crud.get_current_active_user)):
    return await crud.OrderRepository.delete_order_user(current_user=current_user, 
                                  order_id=ordine_id, 
                                  db=db)