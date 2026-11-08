import pytest

from App.crud import (
    UserRepository,
    ArticoloRepository,
    OrderRepository
)

from App.models import (
    UserCreate,
    ArticoloCreate,
    OrderCreate,
    OrderArt
)


from fastapi import HTTPException
from Tests.conftest import CreateOrderSetup



@pytest.mark.anyio
async def test_create_order(db_session):
    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    assert order is not None
    assert order.total == float(10)
    assert order.id == 1


@pytest.mark.anyio
async def test_create_order_articolo_not_existing(db_session):

    user = await CreateOrderSetup.create_user(db_session)

    order_art = OrderArt(
        articolo_id = 1,
        quantità = 1
    )

    new_order = OrderCreate(
        articoli=[
            order_art
        ]
    )

    with pytest.raises(HTTPException) as exc_info:
        await OrderRepository.create_order(
            db = db_session,
            ordine = new_order,
            current_user = user
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo 1 non trovato"


@pytest.mark.anyio
async def test_create_order_giacenza_articolo_non_disponibile(db_session):
    new_user = UserCreate(
            first_name = "Mario",
            last_name = "Rossi",
            email = "mario.rossi@gmail.com",
            password = "123"
        )
        
    user = await UserRepository.create_user(
        db = db_session,
        new_user = new_user
    )

    new_articolo = ArticoloCreate(
            name = "Test",
            desc = "Test",
            prezzo = 20,
            quantità = 20
        )
    
    await ArticoloRepository.create_articolo(
        db = db_session,
        articolo = new_articolo
    )

    order_art = OrderArt(
            articolo_id = 1,
            quantità = 21
        )
    
    new_order = OrderCreate(
        articoli=[
            order_art
        ]
    )

    with pytest.raises(HTTPException) as exc_info:
        await OrderRepository.create_order(
            db = db_session,
            ordine = new_order,
            current_user = user
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Giacenza insufficente per Test. Disponibili : 20"


@pytest.mark.anyio
async def test_lista_ordini_empty(db_session):

    lista = await OrderRepository.all_orders(
        db = db_session
    )

    assert lista == []

@pytest.mark.anyio
async def test_lista_ordini(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    lista = await OrderRepository.all_orders(
        db = db_session
    )

    assert lista is not None
    assert len(lista) == 1

@pytest.mark.anyio
async def test_delete_order_admin(db_session):
    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    delete_order = await OrderRepository.delete_order_admin(
        order_id = 1,
        db = db_session
        )

    assert delete_order == "Ordine con id 1 eliminato!"


@pytest.mark.anyio
async def test_delete_order_admin_order_not_existing(db_session):


    with pytest.raises(HTTPException) as exc_info:
        await OrderRepository.delete_order_admin(
            order_id = 1,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Ordine con id : 1 non trovato"

@pytest.mark.anyio
async def test_get_user_orders(db_session):
    
    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    lista_ordini_user = await OrderRepository.get_user_orders(
        user_id = 1,
        db = db_session
    )

    assert lista_ordini_user is not None
    assert len(lista_ordini_user) == 1

@pytest.mark.anyio
async def test_get_user_orders_user_not_existing(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    with pytest.raises(HTTPException) as exc_info:
        await OrderRepository.get_user_orders(
            user_id = 2,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User con id : 2 non trovato"


@pytest.mark.anyio
async def test_delete_order_user_side(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    article = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = article
    )

    delete_order = await OrderRepository.delete_order_user(
        current_user = user,
        order_id = 1,
        db = db_session
    )

    assert delete_order == "Ordine con id 1 eliminato con successo"

@pytest.mark.anyio
async def test_delete_order_user_side_order_id_not_yours(db_session):

    user1 = await CreateOrderSetup.create_user(db_session)
    user2 = await CreateOrderSetup.create_user2(db_session)
    article = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user1,
        articolo = article
    )

    with pytest.raises(HTTPException) as exc_info:
        await OrderRepository.delete_order_user(
            current_user = user2,
            order_id = 1,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ID non presente nei tuoi ordini o non hai nessun ordine attivo."


@pytest.mark.anyio
async def test_dettagli_ordine(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    dettagli = await OrderRepository.dettagli_ordine(
        current_user = user,
        order_id = order.id,
        db = db_session
    )

    assert dettagli is not None
    assert len(dettagli) == 1

@pytest.mark.anyio
async def test_dettagli_ordine_not_yours(db_session):

    user1 = await CreateOrderSetup.create_user(db_session)
    user2 = await CreateOrderSetup.create_user2(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user1,
        articolo = articolo
    )

    with pytest.raises(HTTPException) as exc_info:
        await OrderRepository.dettagli_ordine(
            current_user = user2,
            order_id = order.id,
            db = db_session  
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ID non presente nei tuoi ordini o non hai nessun ordine attivo."









