import pytest
from fastapi import HTTPException
from Tests.conftest import CreateOrderSetup, Payloads
from App.models import ArticoloCreate
from App.crud import ArticoloRepository


@pytest.mark.anyio
async def test_create_user_seller(db_session):

    seller = await CreateOrderSetup.create_seller(db=db_session)

    assert seller is not None


@pytest.mark.anyio
async def test_create_user_seller_existing(db_session):

    user = await CreateOrderSetup.create_seller(db=db_session)

    with pytest.raises(HTTPException) as exc_info:
        await CreateOrderSetup.create_seller(db=db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"{user.email} già esistente"


@pytest.mark.anyio
async def test_sell_article(db_session):

    seller = await CreateOrderSetup.create_seller(db=db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    assert articolo is not None


@pytest.mark.anyio
async def test_sell_article_existing(db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    with pytest.raises(HTTPException) as exc_info:
        await CreateOrderSetup.create_article(seller=seller, db=db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"{articolo.name} già esistente!"


@pytest.mark.anyio
async def test_sell_article_quantita_non_valida(db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo_create = ArticoloCreate(
        name="testtt", desc="testtt", prezzo=10, quantità=0, category="casa"
    )

    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.create_articolo(
            current_user=seller, db=db_session, articolo=articolo_create
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Quantità : {articolo_create.quantità} non valida"


@pytest.mark.anyio
async def test_sell_article_prezzo_non_valido(db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo_create = ArticoloCreate(
        name="testttt", desc="testttt", prezzo=0, quantità=10, category="casa"
    )

    with pytest.raises(HTTPException) as exc_info:
        await ArticoloRepository.create_articolo(
            current_user=seller, db=db_session, articolo=articolo_create
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Prezzo: {articolo_create.prezzo} non valido"


@pytest.mark.anyio
async def test_lista_articoli_in_vendita(db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    articoli = await ArticoloRepository.get_articles_selled(
        current_user=seller, db=db_session
    )

    assert articoli is not None
    assert articolo in articoli
