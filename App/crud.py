from fastapi import HTTPException
from sqlalchemy.orm import Session
from App.models import *
from App.schemas import *


#Crea Utente
def create_user(db:Session, new_user:UserCreate) -> object:

    user_exists = db.query(User).filter(User.email == new_user.email).one_or_none()

    if user_exists:
        raise HTTPException(status_code=404, detail=f"{new_user.email} già esistente")

    user = User(first_name = new_user.first_name, last_name = new_user.last_name, email = new_user.email)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


#Tutti gli utenti
def user_list(db:Session) -> list[object]:
    return db.query(User).all()


#Crea Articolo
def create_articolo(db:Session, articolo:ArticoloCreate) -> object:

    articolo_exists = db.query(Articolo).filter(Articolo.name == articolo.name).one_or_none()

    if articolo_exists:
        raise HTTPException(status_code=404, detail=f"{articolo.name} già esistente!")

    articolo = Articolo(name = articolo.name, desc = articolo.desc, prezzo = articolo.prezzo, quantità = articolo.quantità)

    db.add(articolo)
    db.commit()
    db.refresh(articolo)
    return articolo


#Tutti gli articoli
def all_articoli(db:Session) -> list[object]:
    return db.query(Articolo).all()


#Crea Ordine
def create_order(db:Session, ordine:OrderCreate) -> object:

    user_exists = db.query(User).filter(User.id == ordine.user_id).one_or_none()

    if not user_exists:
        raise HTTPException(status_code=404, detail="User inesistente!")

    articoli_ids = [art.articolo_id for art in ordine.articoli]

    articoli_selezionati = db.query(Articolo).filter(Articolo.id.in_(articoli_ids)).all()

    mappa_articoli_db = {art.id: art for art in articoli_selezionati}

    nuovo_ordine = Order(user_id = ordine.user_id)
    db.add(nuovo_ordine)
    db.flush()


    totale_ordine : float = 0.0

    for art_richiesto in ordine.articoli:
        articolo_db = mappa_articoli_db.get(art_richiesto.articolo_id)

        if not articolo_db:
            raise HTTPException(status_code=404, detail=f"Articolo {art_richiesto.articolo_id} non trovato")

        if articolo_db.quantità < art_richiesto.quantità:
            raise HTTPException(status_code=404, detail=f"Giacenza insufficente per {articolo_db.name}. Disponibili : {articolo_db.quantità}")


        articolo_db.quantità -= art_richiesto.quantità

        totale_ordine += articolo_db.prezzo * art_richiesto.quantità

        dettaglio = OrderArticolo(
            order_id = nuovo_ordine.id,
            articolo_id= articolo_db.id,
            quantità_ordinata = art_richiesto.quantità
        )

        db.add(dettaglio)


    nuovo_ordine.total = totale_ordine

    db.commit()
    db.refresh(nuovo_ordine)
    return nuovo_ordine
    

#lista articoli ordinati in base all'id ordine
def lista_articoli_ordinati_by_order_id(order_id:int, db:Session) -> list[object]:

    order_exists = db.query(Order).filter(Order.id == order_id).one_or_none()

    if not order_exists:
        raise HTTPException(status_code=404, detail=f"Ordine con id : {order_id} inesistente!")

    dettagli_ordine = db.query(OrderArticolo).filter(OrderArticolo.order_id == order_exists.id).all()

    return dettagli_ordine

#lista ordini
def all_orders(db:Session):
    return db.query(Order).all()


#Elimina ordine
def delete_order(order_id:int, db:Session) -> None:
    order_exists = db.query(Order).filter(Order.id == order_id).one_or_none()

    if not order_exists:
        raise HTTPException(status_code=404, detail=f"Ordine con id : {order_id} non trovato")

    for dettaglio in order_exists.dettagli_articoli:
        dettaglio.articolo.quantità += dettaglio.quantità_ordinata

    db.delete(order_exists)
    db.commit()

    return f"Ordine con id : {order_id} eliminato"
   

#Elimina articolo
def delete_articolo(articolo_id:int,db:Session) -> None:
    artiolo_exists = db.query(Articolo).filter(Articolo.id == articolo_id).one_or_none()

    if not artiolo_exists:
        raise HTTPException(status_code=404, detail=f"Articolo con id : {articolo_id} non esistente nel database!")

    db.delete(artiolo_exists)
    db.commit()
    return f"Articolo con id : {articolo_id} eliminato dal database!"

#Elimina User
def delete_user(user_id:int, db:Session) -> None:
    user_exists = db.query(User).filter(User.id == user_id).one_or_none()

    if not user_exists:
        raise HTTPException(status_code=404, detail=f"User con id : {user_id} non esistente nel database!")

    db.delete(user_exists)
    db.commit()
    return f"User con id : {user_id} eliminato dal database!"

#Modifica prezzo articolo
def prezzo_articolo(nuovo_prezzo:ModificaPrezzoArticolo, articolo_id:int, db:Session) -> None:
    articolo_exists = db.query(Articolo).filter(Articolo.id == articolo_id).one_or_none()

    if not articolo_exists:
        raise HTTPException(status_code=404, detail=f"Articolo con id : {articolo_id} non trovato")

    articolo_exists.prezzo = nuovo_prezzo.prezzo
    db.commit() 
    return articolo_exists

#Aggiungi quantità disponibile
def modifica_giacenza(articolo_id:int, nuova_giacenza:ModificaGiacenzaArticolo, db:Session) -> None:
    articolo_exists = db.query(Articolo).filter(Articolo.id == articolo_id).one_or_none()

    if not articolo_exists:
        raise HTTPException(status_code=404, detail=f"Articolo con id : {articolo_id} non trovato")

    articolo_exists.quantità += nuova_giacenza.quantità
    db.commit()
    return articolo_exists

#Visualizza tutti gli ordini di un utente
def get_user_orders(user_id:int, db:Session) -> list[object]:
    user_exists = db.query(User).filter(User.id == user_id).one_or_none()

    if not user_exists:
        raise HTTPException(status_code=404, detail=f"User con id : {user_id} non trovato")

    return user_exists.orders
