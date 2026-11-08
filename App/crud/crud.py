from fastapi import HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from App.models import User, Articolo, OrderArticolo, Order
from App.config import settings

from App.models import ( TokenData,
                         UserCreate,
                         ArticoloCreate,
                         OrderCreate,
                         ModificaGiacenzaArticolo,
                         ModificaPrezzoArticolo,
                         OrderArt)

from App.auth import (oauth2_scheme,
                      OAuth2PasswordRequestForm,
                      verify_pwd,
                      verify_token,
                      create_access_token,
                      get_pwd_hash)

from App.db import get_session

from datetime import timedelta


#Get user token
async def get_current_user(token:str = Depends(oauth2_scheme), db:AsyncSession = Depends(get_session)) -> User:

    token_data = verify_token(token)
    result = await db.execute(select(User).filter(User.email == token_data.email))
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"Utente {user.email} non esistente"
        )
    return user

#Utente attivo
async def get_current_active_user(current_user : User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=404,
            detail=f"User inattivo"
        )
    return current_user

#Admin
async def get_current_admin_user(current_user:User = Depends(get_current_active_user)) -> User:
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=404,
            detail="Non hai i permessi per accedere a questa pagina"
        )

    return current_user

#Login per Token
async def login_for_access_token(form_data:OAuth2PasswordRequestForm, db:AsyncSession) -> TokenData:
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().one_or_none()

    if not user or not verify_pwd(form_data.password, user.hashed_pwd):
        raise HTTPException(
            status_code=404,
            detail="Username o password errati!"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=404,
            detail="User Inattivo"
        )

    access_token_expires = timedelta(minutes=settings.token_expires)
    access_token = create_access_token(
        data={"sub":user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type":"bearer"}


async def check_users_orders(user:User, order_id:int, db:AsyncSession):
    result = await db.execute(select(Order).filter(Order.id == order_id, Order.user_id == user.id))
    order = result.scalars().one_or_none()
    return order is not None



class UserRepository():

    #Crea Utente
    @staticmethod
    async def create_user(db:AsyncSession, new_user:UserCreate) -> User:

        result = await db.execute(select(User).filter(User.email == new_user.email))
        user_exists = result.scalars().one_or_none()

        if user_exists:
            raise HTTPException(status_code=404, detail=f"{new_user.email} già esistente")

        hashed_password = get_pwd_hash(new_user.password)

        user = User(first_name = new_user.first_name, 
                    last_name = new_user.last_name, 
                    email = new_user.email, 
                    hashed_pwd=hashed_password
                    )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    #Tutti gli utenti
    @staticmethod
    async def user_list(db:AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return list(result.scalars().all())

    #Elimina User
    @staticmethod
    async def delete_user(user_id:int, db:AsyncSession) -> str:
        result = await db.execute(select(User).filter(User.id == user_id))
        user_exists = result.scalars().one_or_none()

        if not user_exists:
            raise HTTPException(status_code=404, detail=f"User con id : {user_id} non esistente nel database!")

        await db.delete(user_exists)
        await db.commit()
        return f"User con id : {user_id} eliminato dal database!"


class ArticoloRepository():

    #Crea Articolo
    @staticmethod
    async def create_articolo(db:AsyncSession, articolo:ArticoloCreate) -> Articolo:

        result = await db.execute(select(Articolo).filter(Articolo.name == articolo.name))
        articolo_exists = result.scalars().one_or_none()

        if articolo_exists:
            raise HTTPException(status_code=404, detail=f"{articolo.name} già esistente!")

        nuovo_articolo = Articolo(name = articolo.name, desc = articolo.desc, prezzo = articolo.prezzo, quantità = articolo.quantità)

        db.add(nuovo_articolo)
        await db.commit()
        await db.refresh(nuovo_articolo)
        return nuovo_articolo

    #Tutti gli articoli
    @staticmethod
    async def all_articoli(db:AsyncSession) -> list[Articolo]:
        result = await db.execute(select(Articolo))
        return list(result.scalars().all())


    #lista articoli ordinati in base all'id ordine
    @staticmethod
    async def lista_articoli_ordinati_by_order_id(order_id:int, db:AsyncSession) -> list[OrderArticolo]:

        result_order = await db.execute(select(Order).filter(Order.id == order_id))
        order_exists = result_order.scalars().one_or_none()

        if not order_exists:
            raise HTTPException(status_code=404, detail=f"Ordine con id : {order_id} inesistente!")

        result_dettagli = await db.execute(select(OrderArticolo).filter(OrderArticolo.order_id == order_exists.id))
        return list(result_dettagli.scalars().all())

    #Elimina articolo
    @staticmethod
    async def delete_articolo(articolo_id:int,db:AsyncSession) -> str:
        result = await db.execute(select(Articolo).filter(Articolo.id == articolo_id))
        articolo_exists = result.scalars().one_or_none()

        if not articolo_exists:
            raise HTTPException(status_code=404, detail=f"Articolo con id : {articolo_id} non esistente nel database!")

        await db.delete(articolo_exists)
        await db.commit()
        return f"Articolo con id : {articolo_id} eliminato dal database!"


    #Modifica prezzo articolo
    @staticmethod
    async def prezzo_articolo(nuovo_prezzo:ModificaPrezzoArticolo, articolo_id:int, db:AsyncSession) -> None:
        result = await db.execute(select(Articolo).filter(Articolo.id == articolo_id))
        articolo_exists = result.scalars().one_or_none()

        if not articolo_exists:
            raise HTTPException(status_code=404, detail=f"Articolo con id : {articolo_id} non trovato")

        articolo_exists.prezzo = nuovo_prezzo.prezzo

        await db.commit()
        await db.refresh(articolo_exists)
        return articolo_exists

    #Aggiungi quantità disponibile
    @staticmethod
    async def modifica_giacenza(articolo_id:int, nuova_giacenza:ModificaGiacenzaArticolo, db:AsyncSession) -> Articolo:
        result = await db.execute(select(Articolo).filter(Articolo.id == articolo_id))
        articolo_exists = result.scalars().one_or_none()

        if not articolo_exists:
            raise HTTPException(status_code=404, detail=f"Articolo con id : {articolo_id} non trovato")

        articolo_exists.quantità += nuova_giacenza.quantità
        await db.commit()
        await db.refresh(articolo_exists)
        return articolo_exists


    #Modifica quantità articoli ordinati
    @staticmethod
    async def edit_order(current_user:User, nuova_quantità:OrderArt, order_id:int, db:AsyncSession) -> OrderArticolo:

        if not await check_users_orders(user=current_user, 
                                    order_id=order_id, db=db):
                raise HTTPException(
                    status_code=404,
                    detail=f"Ordine con id {order_id} non trovato nei tuoi ordini"
                )

        result = await db.execute(
            select(Order)
            .filter(Order.id == order_id)
            .options(selectinload(Order.dettagli_articoli))
        )

        order_exists = result.scalars().one_or_none()

        if not order_exists:
            raise HTTPException(status_code=404, detail=f"Ordine con id : {order_id} non trovato")

        #Mappa dettaglio e articolo singolo tramite articolo_id
        dettagli = order_exists.dettagli_articoli
        dettagli_mappa = {art.articolo_id: art for art in dettagli}
        dettaglio = dettagli_mappa.get(nuova_quantità.articolo_id)

        if not dettaglio:
                raise HTTPException(
                    status_code=404,
                    detail=f"Articolo non esistente"
                )
        
        result_art = await db.execute(select(Articolo).filter(Articolo.id == nuova_quantità.articolo_id))
        articolo = result_art.scalars().one_or_none()

        if not articolo:
            raise HTTPException(
                status_code=404,
                detail=f"Articolo con id : {nuova_quantità.articolo_id} non trovato nell'ordine"
            )

        giacenza_reale_disponibile = articolo.quantità + dettaglio.quantità_ordinata

        if giacenza_reale_disponibile < nuova_quantità.quantità:
            raise HTTPException(
                status_code=404,
                detail=f"Quantità selezionata non disponibile in magazzino, giacenza totale disponibile: {giacenza_reale_disponibile}"
            )

        # Sottrae il costo della quantità dell'articolo precedente dal totale
        prezzo_articolo_precedente = dettaglio.quantità_ordinata * articolo.prezzo
        order_exists.total -= prezzo_articolo_precedente

        # Aggiorna giacenze magazzino ripristinando il vecchio e applicando il nuovo
        articolo.quantità += dettaglio.quantità_ordinata
        dettaglio.quantità_ordinata = nuova_quantità.quantità
        articolo.quantità -= nuova_quantità.quantità 

        # Ricalcola e aggiunge il costo totale aggiornato
        order_exists.total += articolo.prezzo * dettaglio.quantità_ordinata
        
        await db.commit()
        await db.refresh(dettaglio)
        return dettaglio


    #Delete articolo in ordine
    @staticmethod
    async def delete_order_articolo(current_user:User, order_id:int, articolo_id:int, db:AsyncSession) -> None:

        if not await check_users_orders(user=current_user, 
                                order_id=order_id,
                                db=db):
            
            raise HTTPException(
                status_code=404,
                detail=f"Ordine con id {order_id} non trovato nei tuoi ordini"
            )
        
        result_order = await db.execute(select(Order).filter(Order.id == order_id))
        order_exists = result_order.scalars().one_or_none()

        if not order_exists:
            raise HTTPException(
                status_code=404, 
                detail=f"Ordine con id : {order_id} trovato"
            )

        result_detail = await db.execute(select(OrderArticolo).where(OrderArticolo.order_id == order_id, OrderArticolo.articolo_id == articolo_id))
        order_articolo = result_detail.scalar_one_or_none()

        if not order_articolo:
            raise HTTPException(
                status_code=404, 
                detail=f"Articolo con id : {articolo_id} non trovato nell'ordine"
            )
        
        result_art = await db.execute(select(Articolo).filter(Articolo.id == articolo_id))
        articolo = result_art.scalar_one_or_none()

        #Calcolo prezzo totale degli articoli rimossi usando l'oggetto articolo recuperato
        prezzo_articoli = articolo.prezzo * order_articolo.quantità_ordinata
        order_exists.total -= prezzo_articoli

        #Ripristina la merce nel magazzino
        articolo.quantità += order_articolo.quantità_ordinata

        #Se l'ordine si svuota completamente o va sotto zero, lo cancelliamo del tutto
        if order_exists.total <= 0:
            await db.delete(order_exists)
            await db.commit()
            return f"Articolo con id : {articolo_id} eliminato dall'ordine con id : {order_exists.id}. Ordine con id {order_exists.id} eliminato, nessun articolo presente nell'ordine"

        await db.delete(order_articolo)
        await db.commit()
        return f"Articolo con id : {articolo_id} eliminato dall'ordine con id : {order_exists.id}, totale ordine = {order_exists.total}"


class OrderRepository():

    #Crea Ordine
    @staticmethod
    async def create_order(db:AsyncSession, ordine:OrderCreate, current_user:User) -> Order:

        result = await db.execute(select(User).filter(User.id == current_user.id))
        user_exists = result.scalars().one_or_none()

        if not user_exists:
            raise HTTPException(status_code=404, detail="User inesistente!")

        #Trova tutti gli id in user input (OrderCreate)
        articoli_ids = [art.articolo_id for art in ordine.articoli]

        #Cerca gli articoli selezionati nel database
        result_art = await db.execute(select(Articolo).filter(Articolo.id.in_(articoli_ids)))
        articoli_selezionati = result_art.scalars().all()

        #Trasforma gli articoli selezionati in un dizionario, trova l'articolo facilente tramite l'id 
        mappa_articoli_db = {art.id: art for art in articoli_selezionati}

        #Crea l'ordine
        nuovo_ordine = Order(user_id = current_user.id)
        db.add(nuovo_ordine)
        await db.flush()


        totale_ordine : float = 0.0

        #Controlla se l'articolo richiesto è esistente e se la giacenza è sufficiente
        for art_richiesto in ordine.articoli:
            articolo_db = mappa_articoli_db.get(art_richiesto.articolo_id)

            if not articolo_db:
                raise HTTPException(status_code=404, detail=f"Articolo {art_richiesto.articolo_id} non trovato")

            if articolo_db.quantità < art_richiesto.quantità:
                raise HTTPException(status_code=404, detail=f"Giacenza insufficente per {articolo_db.name}. Disponibili : {articolo_db.quantità}")

            #Toglie la quantità dal magazzino
            articolo_db.quantità -= art_richiesto.quantità

            #Aggiorna il totale dell'ordine
            totale_ordine += articolo_db.prezzo * art_richiesto.quantità

            #Crea l'ordine
            dettaglio = OrderArticolo(
                order_id = nuovo_ordine.id,
                articolo_id= articolo_db.id,
                quantità_ordinata = art_richiesto.quantità
            )

            db.add(dettaglio)


        nuovo_ordine.total = totale_ordine

        await db.commit()
        await db.refresh(nuovo_ordine)
        return nuovo_ordine


    #lista ordini
    @staticmethod
    async def all_orders(db:AsyncSession) -> list[Order]:
        result = await db.execute(select(Order))
        return list(result.scalars().all())

    #Elimina ordine
    @staticmethod
    async def delete_order_admin(order_id:int, db:AsyncSession) -> str:

        result = await db.execute(select(Order).filter(Order.id == order_id))
        order_exists = result.scalars().one_or_none()

        if not order_exists:
            raise HTTPException(status_code=404, detail=f"Ordine con id : {order_id} non trovato")

        result_dettagli = await db.execute(select(OrderArticolo).filter(OrderArticolo.order_id == order_id))
        dettagli = result_dettagli.scalars().all()

        for dettaglio in dettagli:
            res_art = await db.execute(select(Articolo).filter(Articolo.id == dettaglio.articolo_id))
            art = res_art.scalars().one()
            art.quantità += dettaglio.quantità_ordinata

        await db.delete(order_exists)
        await db.commit()
        return f"Ordine con id {order_id} eliminato!"


    #Visualizza tutti gli ordini di un utente
    @staticmethod
    async def get_user_orders(user_id:int, db:AsyncSession) -> list[Order]:
        result_user = await db.execute(select(User).filter(User.id == user_id))
        user_exists = result_user.scalars().one_or_none()

        if not user_exists:
            raise HTTPException(status_code=404, detail=f"User con id : {user_id} non trovato")

        result_orders = await db.execute(select(Order).filter(Order.user_id == user_id))

        return list(result_orders.scalars().all())

    #Elimina l'intero ordine lato utente
    @staticmethod
    async def delete_order_user(current_user:User, order_id:int, db:AsyncSession) -> str:

        if not await check_users_orders(user=current_user,
                                        order_id=order_id,
                                        db=db):
            raise HTTPException(
                status_code=404,
                detail="ID non presente nei tuoi ordini o non hai nessun ordine attivo."
            )

        result = await db.execute(
            select(Order)
            .filter(Order.id == order_id)
            .options(selectinload(Order.dettagli_articoli))
        )

        ordine = result.scalars().one_or_none()

        if not ordine:
            raise HTTPException(
                status_code=404,
                detail=f"Ordine non trovato"
            )

        # Ripristino magazzino per ogni articolo presente nell'ordine
        for dettaglio in ordine.dettagli_articoli:
            result_art = await db.execute(select(Articolo).filter(Articolo.id == dettaglio.articolo_id))
            art = result_art.scalars().one()
            art.quantità += dettaglio.quantità_ordinata

        await db.delete(ordine)
        await db.commit()
        return f"Ordine con id {order_id} eliminato con successo"

    @staticmethod
    async def dettagli_ordine(current_user:User, order_id:int, db:AsyncSession):

        result_order = await db.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.dettagli_articoli)))

        order_exists = result_order.scalar_one_or_none()

        if not await check_users_orders(user=current_user, order_id=order_id, db=db):
            raise HTTPException(
                status_code=404,
                detail="ID non presente nei tuoi ordini o non hai nessun ordine attivo."
            )

        dettagli = order_exists.dettagli_articoli

        return list(dettagli)



