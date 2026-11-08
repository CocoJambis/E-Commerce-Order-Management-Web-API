import pytest

from App.crud import (
    ArticoloRepository
    )

from App.models import (
    ModificaPrezzoArticolo,
    ModificaGiacenzaArticolo,
    OrderArt
)

from fastapi import HTTPException
from Tests.conftest import CreateOrderSetup


@pytest.mark.anyio
async def test_create_articolo(db_session):

    articolo = await CreateOrderSetup.create_article(db_session)

    assert articolo is not None
    assert articolo.name == "Test"
    assert articolo.desc == "Test"
    assert articolo.prezzo == articolo.prezzo
    assert articolo.quantità == articolo.quantità

@pytest.mark.anyio
async def test_create_articolo_existing(db_session):

    articolo = await CreateOrderSetup.create_article(db_session)

    with pytest.raises(HTTPException) as exc_info:
        articolo2 = await CreateOrderSetup.create_article(db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"{articolo.name} già esistente!"


@pytest.mark.anyio
async def test_list_all_articoli(db_session):

    articolo1 = await CreateOrderSetup.create_article(db_session)
    articolo2 = await CreateOrderSetup.create_article2(db_session)

    list_articoli = await ArticoloRepository.all_articoli(db = db_session)

    assert list_articoli is not None
    assert len(list_articoli) == 2
    assert list_articoli[0].name == "Test"
    assert list_articoli[1].name == "Test2"


@pytest.mark.anyio
async def test_lista_articoli_ordinati_by_order_id(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    articoli = await ArticoloRepository.lista_articoli_ordinati_by_order_id(order_id = order.id, db = db_session)
    
    assert articoli is not None
    assert len(articoli) == 1


@pytest.mark.anyio
async def test_lista_articoli_ordinati_by_order_id_not_existing(db_session):


    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.lista_articoli_ordinati_by_order_id(order_id = 1, db = db_session)


    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Ordine con id : 1 inesistente!"


@pytest.mark.anyio
async def test_delete_articolo(db_session):

    articolo = await CreateOrderSetup.create_article(db_session)

    articolo_delete = await ArticoloRepository.delete_articolo(articolo.id, db = db_session)

    assert articolo_delete == "Articolo con id : 1 eliminato dal database!"


@pytest.mark.anyio
async def test_delete_articolo_not_existing(db_session):


    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.delete_articolo(articolo_id = 1, db = db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo con id : 1 non esistente nel database!"


@pytest.mark.anyio
async def test_modifica_prezzo_articolo(db_session):

    articolo = await CreateOrderSetup.create_article(db_session)

    assert articolo.prezzo == 10

    nuovo_prezzo = ModificaPrezzoArticolo(
        prezzo = 20
    )

    await ArticoloRepository.prezzo_articolo(
        nuovo_prezzo = nuovo_prezzo, 
        articolo_id = 1, 
        db = db_session)

    assert articolo.prezzo == 20


@pytest.mark.anyio
async def test_modifica_prezzo_articolo_not_existing(db_session):

    nuovo_prezzo = ModificaPrezzoArticolo(
            prezzo = 20
        )

    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.prezzo_articolo(
            nuovo_prezzo = nuovo_prezzo,
            articolo_id = 1,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo con id : 1 non trovato"


@pytest.mark.anyio
async def test_modifica_giacenza_articolo(db_session):

    articolo = await CreateOrderSetup.create_article(db_session)


    nuova_giacenza = ModificaGiacenzaArticolo(
        quantità = 30
    )

    assert articolo.quantità == 20

    result = await ArticoloRepository.modifica_giacenza(
        articolo_id = articolo.id,
        nuova_giacenza = nuova_giacenza,
        db = db_session
    )

    assert result.quantità == 50


@pytest.mark.anyio
async def test_modifica_giacenza_articolo_not_existing(db_session):


    nuova_giacenza = ModificaGiacenzaArticolo(
        quantità = 10
    )


    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.modifica_giacenza(
            articolo_id = 1,
            nuova_giacenza = nuova_giacenza,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo con id : 1 non trovato"


@pytest.mark.anyio
async def test_edit_order(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )


    articolo_edit_order = OrderArt(
        articolo_id=articolo.id,
        quantità = 2
    )


    edit = await ArticoloRepository.edit_order(
        current_user= user,
        nuova_quantità = articolo_edit_order,
        order_id = order.id,
        db = db_session
    )

    assert edit.quantità_ordinata == 2
    assert edit.articolo_id == 1
    assert edit.order_id == 1


@pytest.mark.anyio
async def test_edit_order_not_existing(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)

    articolo_order = OrderArt(
        articolo_id = 1,
        quantità = 1
    )

    articolo_edit_order = OrderArt(
        articolo_id=1,
        quantità = 2
    )


    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.edit_order(
            current_user= user,
            nuova_quantità = articolo_edit_order,
            order_id = 1,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Ordine con id 1 non trovato nei tuoi ordini"


@pytest.mark.anyio
async def test_edit_order_not_yours(db_session):

    user1 = await CreateOrderSetup.create_user(db_session)
    user2 = await CreateOrderSetup.create_user2(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user1,
        articolo = articolo
    )

    nuova_quantità = OrderArt(
        articolo_id = articolo.id,
        quantità = 2
    )


    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.edit_order(
            current_user = user2,
            nuova_quantità= nuova_quantità,
            order_id = 1,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Ordine con id 1 non trovato nei tuoi ordini"


@pytest.mark.anyio
async def test_edit_order_articolo_not_existing(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    edit_order = OrderArt(
        articolo_id = 2,
        quantità = 2
    )

    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.edit_order(
            current_user = user,
            nuova_quantità = edit_order,
            order_id = order.id,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo non esistente"


@pytest.mark.anyio
async def test_edit_order_giacenza_articolo_non_disponibile(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )

    edit_order = OrderArt(
        articolo_id = 1,
        quantità = 21
    )


    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.edit_order(
            current_user = user,
            nuova_quantità = edit_order,
            order_id = 1,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Quantità selezionata non disponibile in magazzino, giacenza totale disponibile: 20"
    
@pytest.mark.anyio
async def test_delete_order_articolo_then_empty_order(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )
    
    delete = await ArticoloRepository.delete_order_articolo(
            current_user = user,
            order_id = 1,
            articolo_id = 1,
            db = db_session
        )

    assert delete == "Articolo con id : 1 eliminato dall'ordine con id : 1. Ordine con id 1 eliminato, nessun articolo presente nell'ordine"

@pytest.mark.anyio
async def test_delete_order_art_order_not_empty(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo1 = await CreateOrderSetup.create_article(db_session)
    articolo2 = await CreateOrderSetup.create_article2(db_session)
    order = await CreateOrderSetup.create_order2(
        db = db_session,
        user = user,
        articolo1 = articolo1,
        articolo2 = articolo2
    )

    delete_art = await ArticoloRepository.delete_order_articolo(
        current_user = user,
        order_id = order.id,
        articolo_id = articolo1.id,
        db = db_session
    )


    assert delete_art == f"Articolo con id : {articolo1.id} eliminato dall'ordine con id : {order.id}, totale ordine = {order.total}"


@pytest.mark.anyio
async def test_delete_order_articolo_articolo_id_not_exsisting(db_session):

    user = await CreateOrderSetup.create_user(db_session)
    articolo = await CreateOrderSetup.create_article(db_session)
    order = await CreateOrderSetup.create_order(
        db = db_session,
        user = user,
        articolo = articolo
    )


    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.delete_order_articolo(
            current_user = user,
            order_id = order.id,
            articolo_id = 2,
            db = db_session
        )


    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Articolo con id : 2 non trovato nell'ordine"


@pytest.mark.anyio
async def test_delete_order_art_order_not_existing(db_session):

    user = await CreateOrderSetup.create_user(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.delete_order_articolo(
            current_user = user,
            order_id = 1,
            articolo_id = 1,
            db = db_session
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Ordine con id 1 non trovato nei tuoi ordini"

