from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from App.db import get_session
from App.models import ( ArticoloResponse,
                         ArticoloCreate,
                         ModificaPrezzoArticolo,
                         ModificaGiacenzaArticolo,
                         UserResponse,
                         OrderResponse,
                         ArticoliOrdinati)
from App.crud import crud 

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(crud.get_current_admin_user)]
)

#---------------------ARTICOLI--------------------------

#Crea articolo
@router.post("/articolo", response_model=ArticoloResponse)
async def crea_articolo(articolo:ArticoloCreate, db:AsyncSession = Depends(get_session)):
    return await crud.ArticoloRepository.create_articolo(db=db, articolo=articolo)

#Modifica prezzo articolo
@router.put("/{articolo_id}", response_model=ArticoloResponse)
async def modifica_prezzo_articolo(nuovo_prezzo:ModificaPrezzoArticolo, articolo_id:int, db:AsyncSession = Depends(get_session)):
    return await crud.ArticoloRepository.prezzo_articolo(nuovo_prezzo=nuovo_prezzo, articolo_id=articolo_id, db=db)

#Aggiungi quantità articolo
@router.put("/aggiungigiacenza/{articolo_id}", response_model=ArticoloResponse)
async def aggiungi_quantità(nuova_quantità:ModificaGiacenzaArticolo, articolo_id:int, db:AsyncSession = Depends(get_session)):
    return await crud.ArticoloRepository.modifica_giacenza(articolo_id=articolo_id, nuova_giacenza=nuova_quantità, db=db)

#Elimina articolo
@router.delete("/articolo/{articolo_id}")
async def delete_articolo(articolo_id:int, db:AsyncSession = Depends(get_session)):
    return await crud.ArticoloRepository.delete_articolo(articolo_id=articolo_id, db=db)


#---------------------USERS--------------------------

#Lista tutti gli utenti
@router.get("/users", response_model=list[UserResponse])
async def all_users(db:AsyncSession = Depends(get_session)):
    return await crud.UserRepository.user_list(db=db)

#Elimina utente
@router.delete("/user/{user_id}")
async def delete_user(user_id:int, db:AsyncSession = Depends(get_session)):
    return await crud.UserRepository.delete_user(user_id=user_id, db=db)


#---------------------ORDERS--------------------------

#Tutti gli ordini
@router.get("/orders", response_model=list[OrderResponse])
async def all_orders(db:AsyncSession = Depends(get_session)):
    return await crud.OrderRepository.all_orders(db=db)

#Lista articoli ordinati in un ordine
@router.get("/articoliordinati/{order_id}", response_model=list[ArticoliOrdinati])
async def lista_articoli_ordinati(order_id:int, db:AsyncSession = Depends(get_session)):
    return await crud.ArticoloRepository.lista_articoli_ordinati_by_order_id(order_id=order_id, db=db)

#Elimina ordine
@router.delete("/orders/{order_id}")
async def delete_order(order_id:int, db:AsyncSession = Depends(get_session)):
    return await crud.OrderRepository.delete_order_admin(order_id=order_id, db=db)
