import pytest
from fastapi import HTTPException
from App.models import *
from App.schemas import *
from App.crud import *



def test_create_user(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db = db_session, new_user=user_in)

    assert user.first_name == "Mario"
    assert user.last_name == "Rossi"
    assert user.email == "mario.rossi@gmail.com"


def test_create_user_already_existing(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    create_user(db=db_session, new_user=user_in)

    with pytest.raises(HTTPException) as exc_info:
        create_user(db=db_session, new_user=user_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "mario.rossi@gmail.com già esistente"


def test_create_articolo(db_session):
    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)

    assert articolo.name == "test"
    assert articolo.desc == "test"
    assert articolo.quantità == 20


def test_create_articolo_già_esistente(db_session):
    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    create_articolo(db= db_session, articolo = articolo_in)

    with pytest.raises(HTTPException) as exc_info:
        create_articolo(db=db_session, articolo= articolo_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "test già esistente!"


def test_create_order(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db=db_session, new_user=user_in)

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)


    ordine_in = OrderCreate(user_id = user.id, articoli=[{"articolo_id" : articolo.id, "quantità" : 10}])
    ordine = create_order(db=db_session, ordine= ordine_in)


    assert ordine.user_id == user.id

    for art in ordine.dettagli_articoli:
        assert art.articolo.name == "test"
        assert art.articolo.quantità == 10
        assert art.articolo.prezzo == 10
        assert ordine.total == art.articolo.prezzo * art.quantità_ordinata


def test_create_order_user_not_found(db_session):

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)


    ordine_in = OrderCreate(user_id = "1", articoli=[{"articolo_id" : articolo.id, "quantità" : 10}])

    with pytest.raises(HTTPException) as exc_info:
        ordine = create_order(db=db_session, ordine= ordine_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User inesistente!"

def test_create_order_con_articolo_id_non_esistente(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db=db_session, new_user=user_in)

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)


    ordine_in = OrderCreate(user_id = user.id, articoli=[{"articolo_id" : "3", "quantità" : 10}])

    with pytest.raises(HTTPException) as exc_info:
        create_order(db=db_session, ordine= ordine_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo 3 non trovato"

def test_create_order_quantità_maggiore_giacenza(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db=db_session, new_user=user_in)

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)


    ordine_in = OrderCreate(user_id = user.id, articoli=[{"articolo_id" : articolo.id, "quantità" : 21}])

    with pytest.raises(HTTPException) as exc_info:
        create_order(db=db_session, ordine= ordine_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Giacenza insufficente per test. Disponibili : 20"


def test_lista_articoli_ordinati_by_order_id(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db=db_session, new_user=user_in)

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)


    ordine_in = OrderCreate(user_id = user.id, articoli=[{"articolo_id" : articolo.id, "quantità" : 10}])
    ordine = create_order(db=db_session, ordine= ordine_in)

    assert lista_articoli_ordinati_by_order_id(ordine.id, db=db_session) is not None


def test_delete_user(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db = db_session, new_user=user_in)

    message = delete_user(user_id= user.id, db = db_session)

    assert message == f"User con id : {user.id} eliminato dal database!"

def test_delete_user_not_found(db_session):

    with pytest.raises(HTTPException) as exc_info:
        message = delete_user(user_id= "1", db = db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"User con id : 1 non esistente nel database!"

def test_delete_articolo(db_session):
    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)

    message = delete_articolo(articolo_id=articolo.id, db = db_session)

    assert message == f"Articolo con id : {articolo.id} eliminato dal database!"

def test_delete_articolo_not_found(db_session):

    with pytest.raises(HTTPException) as exc_info:
        delete_articolo(articolo_id= "1", db = db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Articolo con id : 1 non esistente nel database!"

def test_delete_order(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db=db_session, new_user=user_in)

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)


    ordine_in = OrderCreate(user_id = user.id, articoli=[{"articolo_id" : articolo.id, "quantità" : 10}])
    ordine = create_order(db=db_session, ordine= ordine_in)

    message = delete_order(order_id = ordine.id, db = db_session)

    assert message == f"Ordine con id : {ordine.id} eliminato"

def test_delete_order_not_found(db_session):

    with pytest.raises(HTTPException) as exc_info:
        delete_order(order_id = "1", db = db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Ordine con id : 1 non trovato"

def test_prezzo_articolo(db_session):
    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)

    nuovo_prezzo = ModificaPrezzoArticolo(prezzo = 20)

    prezzo_articolo(nuovo_prezzo=nuovo_prezzo, articolo_id = articolo.id, db = db_session)

    assert articolo.prezzo == 20

def test_prezzo_articolo_not_found(db_session):

    nuovo_prezzo = ModificaPrezzoArticolo(prezzo = 20)

    with pytest.raises(HTTPException) as exc_info:
        prezzo_articolo(nuovo_prezzo=nuovo_prezzo, articolo_id = "1", db = db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Articolo con id : 1 non trovato"

def test_modifica_giacenza(db_session):
    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)

    nuova_giacenza = ModificaGiacenzaArticolo(quantità = 2)

    modifica_giacenza(articolo_id = articolo.id, nuova_giacenza=nuova_giacenza, db= db_session)

    assert articolo.quantità == 22

def test_modifica_giacenza_articolo_not_found(db_session):

    nuova_giacenza = ModificaGiacenzaArticolo(quantità = 2)

    with pytest.raises(HTTPException) as exc_info:
        modifica_giacenza(articolo_id="1", nuova_giacenza=nuova_giacenza, db = db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Articolo con id : 1 non trovato"

def test_get_user_orders(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db=db_session, new_user=user_in)

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)


    ordine_in = OrderCreate(user_id = user.id, articoli=[{"articolo_id" : articolo.id, "quantità" : 10}])
    ordine = create_order(db=db_session, ordine= ordine_in)

    ordini_user = get_user_orders(user_id=user.id, db=db_session)

    assert ordini_user is not None

def test_get_user_orders_not_found(db_session):
    user_in = UserCreate(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")
    user = create_user(db=db_session, new_user=user_in)

    articolo_in = ArticoloCreate(name = "test", desc="test", prezzo = 10, quantità=20)
    articolo = create_articolo(db= db_session, articolo = articolo_in)

    ordini_user = get_user_orders(user_id=user.id, db=db_session)

    mappa_ordini_user = {ord.id: ord for ord in ordini_user}

    assert len(ordini_user) == 0
    assert mappa_ordini_user.get(user.id) == None
