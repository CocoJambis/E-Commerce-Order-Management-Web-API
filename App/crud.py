from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from App.models import *
from App.schemas import *
from App.auth import *
from App.db import get_db


#Get user token
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)) -> User:
    token_data = verify_token(token)
    user = db.query(User).filter(User.email == token_data.email).one_or_none()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"Utente {user.email} non esistente"
        )
    return user

#Utente attivo
def get_current_active_user(current_user : User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=404,
            detail=f"User inattivo"
        )
    return current_user

#Admin
def get_current_admin_user(current_user:User = Depends(get_current_active_user)) -> User:
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=404,
            detail="Non hai i permessi per accedere a questa pagina"
        )

    return current_user

#Login per Token
def login_for_access_token(form_data:OAuth2PasswordRequestForm, db:Session) -> TokenData:
    user = db.query(User).filter(User.email == form_data.username).one_or_none()

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

#Crea Utente
def create_user(db:Session, new_user:UserCreate) -> User:

    user_exists = db.query(User).filter(User.email == new_user.email).one_or_none()

    if user_exists:
        raise HTTPException(status_code=404, detail=f"{new_user.email} già esistente")

    hashed_password = get_pwd_hash(new_user.password)

    user = User(first_name = new_user.first_name, 
                last_name = new_user.last_name, 
                email = new_user.email, 
                hashed_pwd=hashed_password
                )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


#Tutti gli utenti
def user_list(db:Session) -> list[User]:
    return db.query(User).all()


#Crea Articolo
def create_articolo(db:Session, articolo:ArticoloCreate) -> Articolo:

    articolo_exists = db.query(Articolo).filter(Articolo.name == articolo.name).one_or_none()

    if articolo_exists:
        raise HTTPException(status_code=404, detail=f"{articolo.name} già esistente!")

    articolo = Articolo(name = articolo.name, desc = articolo.desc, prezzo = articolo.prezzo, quantità = articolo.quantità)

    db.add(articolo)
    db.commit()
    db.refresh(articolo)
    return articolo


#Tutti gli articoli
def all_articoli(db:Session) -> list[Articolo]:
    return db.query(Articolo).all()


#Crea Ordine
def create_order(db:Session, ordine:OrderCreate, current_user:User) -> Order:

    user_exists = db.query(User).filter(User.id == current_user.id).one_or_none()

    if not user_exists:
        raise HTTPException(status_code=404, detail="User inesistente!")

    #Trova tutti gli id in user input (OrderCreate)
    articoli_ids = [art.articolo_id for art in ordine.articoli]

    #Cerca gli articoli selezionati nel database
    articoli_selezionati = db.query(Articolo).filter(Articolo.id.in_(articoli_ids)).all()

    #Trasforma gli articoli selezionati in un dizionario, trova l'articolo facilente tramite l'id 
    mappa_articoli_db = {art.id: art for art in articoli_selezionati}

    #Crea l'ordine
    nuovo_ordine = Order(user_id = current_user.id)
    db.add(nuovo_ordine)
    db.flush()


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

    db.commit()
    db.refresh(nuovo_ordine)
    return nuovo_ordine
    

#lista articoli ordinati in base all'id ordine
def lista_articoli_ordinati_by_order_id(order_id:int, db:Session) -> list[OrderArticolo]:

    order_exists = db.query(Order).filter(Order.id == order_id).one_or_none()

    if not order_exists:
        raise HTTPException(status_code=404, detail=f"Ordine con id : {order_id} inesistente!")

    dettagli_ordine = db.query(OrderArticolo).filter(OrderArticolo.order_id == order_exists.id).all()

    return dettagli_ordine

#lista ordini
def all_orders(db:Session):
    return db.query(Order).all()


#Elimina ordine
def delete_order_admin(order_id:int, db:Session) -> None:
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
def get_user_orders(user_id:int, db:Session) -> list[Order]:
    user_exists = db.query(User).filter(User.id == user_id).one_or_none()

    if not user_exists:
        raise HTTPException(status_code=404, detail=f"User con id : {user_id} non trovato")

    return user_exists.orders


#Modifica quantità articoli ordinati
def edit_order(current_user:User, nuova_quantità:OrderArt, order_id:int, db:Session) -> OrderArticolo:

    ordini_utente = current_user.orders

    orders_ids = [ord.id for ord in ordini_utente]

    if order_id not in orders_ids:
        raise HTTPException(
            status_code=404,
            detail= f"Ordine con id {order_id} non trovato nei tuoi ordini"
        )

    order_exists = db.query(Order).filter(Order.id == order_id).one_or_none()

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
    
    articolo = dettaglio.articolo

    if not articolo:
        raise HTTPException(
            status_code=404,
            detail=f"Articolo con id : {nuova_quantità.articolo_id} non trovato nell'ordine"
        )

    if articolo.quantità < nuova_quantità.quantità:
        raise HTTPException(
            status_code=404,
            detail=f"Quantità selezionata non disponibile in magazzino, giacenza : {dettaglio.articolo.quantità}"
        )

    #Toglie il costo della quantità dell'articolo precedente
    prezzo_articolo = dettaglio.quantità_ordinata * articolo.prezzo
    order_exists.total -= prezzo_articolo

    #Aggiorna giacenze
    articolo.quantità += dettaglio.quantità_ordinata
    dettaglio.quantità_ordinata = nuova_quantità.quantità
    articolo.quantità -= nuova_quantità.quantità 

    #Aggiunge il costo totale
    order_exists.total += articolo.prezzo * dettaglio.quantità_ordinata
    
    db.commit()
    db.refresh(dettaglio)
    return dettaglio

#Delete articolo in ordine
def delete_order_articolo(current_user:User, order_id:int, articolo_id:int, db:Session) -> None:

    if not check_users_orders(user=current_user, 
                              order_id=order_id):
        raise HTTPException(
            status_code=404,
            detail=f"Ordine con id {order_id} non trovato nei tuoi ordini"
        )
    
    order_exists = db.query(Order).filter(Order.id == order_id).one_or_none()

    if not order_exists:
        raise HTTPException(
            status_code=404, 
            detail=f"Ordine con id : {order_id} trovato"
        )

    order_articolo = db.query(OrderArticolo).filter(OrderArticolo.articolo_id == articolo_id).one_or_none()

    if not order_articolo:
        raise HTTPException(
            status_code=404, 
            detail=f"Articolo con id : {articolo_id} non trovato nell'ordine"
        )
    
    articolo = db.query(Articolo).filter(Articolo.id == articolo_id).one_or_none()

    prezzo_articoli = order_articolo.articolo.prezzo * order_articolo.quantità_ordinata

    order_exists.total -= prezzo_articoli

    articolo.quantità += order_articolo.quantità_ordinata

    if order_exists.total <= 0:
        db.delete(order_exists)
        db.commit()
        return f"Articolo con id : {articolo_id} eliminato dall'ordine con id : {order_exists.id}. Ordine con id {order_exists.id} eliminato, nessun articolo presente nell'ordine"

    db.delete(order_articolo)
    db.commit()
    return f"Articolo con id : {articolo_id} eliminato dall'ordine con id : {order_exists.id}, totale ordine = {order_exists.total}"

def delete_order_user(current_user:User, order_id:int, db:Session):

    current_user_orders = current_user.orders

    if not current_user_orders:
        raise HTTPException(
            status_code=404,
            detail=f"Non hai nessun ordine."
        )

    if not check_users_orders(user=current_user,
                              order_id=order_id):
        raise HTTPException(
            status_code=404,
            detail=f"ID non presente nei tuoi ordini"
        )

    ordine = db.query(Order).filter(Order.id == order_id).one_or_none()

    for dettaglio in ordine.dettagli_articoli:
        dettaglio.articolo.quantità += dettaglio.quantità_ordinata

    db.delete(ordine)
    db.commit()
    return f"Ordine con id {order_id} eliminato con successo"


def check_users_orders(user:User, order_id:int):
    ordini = user.orders

    ordini_ids = [ord.id for ord in ordini]

    if order_id not in ordini_ids:
        return False
    else:
        return True
    