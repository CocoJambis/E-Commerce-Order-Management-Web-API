import pytest
from Tests.conftest import CreateOrderSetup


@pytest.mark.anyio
async def test_add_order(client):

    payload = {"articoli": [{"articolo_id": 1, "quantità": 20}]}

    response = await client.post("/ordini", json=payload)

    assert response.status_code == 401


@pytest.mark.anyio
async def test_modifica_quantità_articolo_ordinata(client, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)
    order = await CreateOrderSetup.create_order(
        db=db_session, user=seller, articolo=articolo
    )

    payload = {"articolo_id": 1, "quantità": 20}

    response = await client.put(f"/ordini/ordinearticolo/{order.id}", json=payload)

    assert response.status_code == 401, f"Errore {response.text}"


@pytest.mark.anyio
async def test_delete_articolo_from_order(client, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)
    order = await CreateOrderSetup.create_order(
        db=db_session, user=seller, articolo=articolo
    )

    response = await client.delete(f"/ordini/articolo/{order.id}/{articolo.id}")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_delete_order(client):

    response = await client.delete("/ordini/delete/1")

    assert response.status_code == 401
