import pytest
from fastapi import HTTPException
from Tests.conftest import CreateOrderSetup
from App.crud import CartRepository
from App.models import OrderArt


@pytest.mark.anyio
async def test_add_to_cart(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(seller= user, db= db_session)

    payload_art = OrderArt(
        articolo_id= articolo.id,
        quantità= 1
    )

    riga_carrello = await CartRepository.add_to_cart(
        payload = payload_art,
        current_user= user,
        db= db_session
    )

    assert riga_carrello is not None
    assert riga_carrello.quantity == 1
    assert riga_carrello.prezzo == 10
    assert riga_carrello.subtotal == 10.00

@pytest.mark.anyio
async def test_add_to_cart_article_not_existing(db_session):

    user = await CreateOrderSetup.create_user(db_session)

    payload = OrderArt(articolo_id=1, quantità=1)


    with pytest.raises(HTTPException) as exc_info:
        await CartRepository.add_to_cart(
            payload= payload,
            current_user= user,
            db= db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Prodotto non trovato"

@pytest.mark.anyio
async def test_add_to_cart_giacenza_non_disponibile(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(seller= user, db= db_session)

    payload = OrderArt(articolo_id= articolo.id, quantità = 200)

    with pytest.raises(HTTPException) as exc_info:
        await CartRepository.add_to_cart(
            payload= payload,
            current_user= user,
            db= db_session
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == f"Disponibilità insufficente. Massimo ordinabile: {articolo.quantità}"

@pytest.mark.anyio
async def test_view_cart(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(seller= user, db= db_session)

    payload = OrderArt(articolo_id= articolo.id, quantità= 1)

    await CartRepository.add_to_cart(payload= payload, current_user= user, db= db_session)

    cart = await CartRepository.view_cart(
        current_user= user,
        db= db_session
    )

    assert cart is not None
    assert len(cart.items) == 1
    assert cart.total_amount == 10.00


@pytest.mark.anyio
async def test_view_cart_empty(db_session):

    user = await CreateOrderSetup.create_user(db_session)

    cart = await CartRepository.view_cart(
        current_user= user,
        db= db_session
    )

    assert len(cart.items) == 0
    assert cart is not None
    assert cart.user_id == user.id


@pytest.mark.anyio
async def test_remove_item_from_cart(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(seller= user, db= db_session)

    payload = OrderArt(articolo_id= articolo.id, quantità= 1)

    await CartRepository.add_to_cart(payload= payload, current_user= user, db= db_session)

    cart = await CartRepository.remove_item_from_cart(
        db= db_session,
        item_id= articolo.id,
        current_user= user,
        quantity=1
    )

    assert len(cart.items) == 0
    assert cart.total_amount == 0.00


@pytest.mark.anyio
async def test_remove_item_from_cart_empty(db_session):

    user = await CreateOrderSetup.create_user(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await CartRepository.remove_item_from_cart(
            db= db_session,
            current_user= user,
            quantity=1,
            item_id= 1
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Il Tuo carrello è vuoto"


@pytest.mark.anyio
async def test_remove_item_from_cart_articolo_not_in_cart(db_session):

    user = await CreateOrderSetup.create_user(db_session)

    articolo = await CreateOrderSetup.create_article(seller= user, db= db_session)

    payload = OrderArt(articolo_id= articolo.id, quantità=1)

    await CartRepository.add_to_cart(
        payload = payload,
        current_user= user,
        db= db_session
    )

    with pytest.raises(HTTPException) as exc_info:
        await CartRepository.remove_item_from_cart(
            db= db_session,
            item_id = 2,
            current_user = user,
            quantity = 1
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo selezionato non presente nel carrello"
    

@pytest.mark.anyio
async def test_remove_item_from_cart_quantity_maggiore_0(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(seller= user, db= db_session)

    payload = OrderArt(articolo_id= articolo.id, quantità=1)

    await CartRepository.add_to_cart(payload= payload, current_user=user, db= db_session)

    with pytest.raises(HTTPException) as exc_info:
        await CartRepository.remove_item_from_cart(
            db= db_session,
            item_id= articolo.id,
            current_user = user,
            quantity= 0
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "La quantità da rimuovere deve essere maggiore di 0"

@pytest.mark.anyio
async def test_remove_item_from_cart_remove_quantity_maggiore(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(seller= user, db= db_session)


    payload = OrderArt(articolo_id= articolo.id, quantità = 1)

    await CartRepository.add_to_cart(payload= payload, current_user= user, db= db_session)

    with pytest.raises(HTTPException) as exc_info:
        await CartRepository.remove_item_from_cart(
            db= db_session,
            item_id= 1,
            current_user= user,
            quantity= 2
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Impossibile togliere quantità maggiore"



    



