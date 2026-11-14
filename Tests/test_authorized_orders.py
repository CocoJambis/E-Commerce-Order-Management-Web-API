import pytest
from Tests.conftest import Payloads, CreateOrderSetup
from sqlalchemy import select
from App.models import User


@pytest.mark.anyio
async def test_create_order(client, user_token, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    order_payload = await Payloads.order_payload()

    response = await client.post("/ordini", headers=headers, json=order_payload)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_modifica_quantità_articolo_ordinata(client, user_token, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)
    result = await db_session.execute(
        select(User).where(User.email == "mario.rossi@gmail.com")
    )
    user = result.scalar_one_or_none()

    order = await CreateOrderSetup.create_order(
        db=db_session, user=user, articolo=articolo
    )

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    payload = {"articolo_id": 1, "quantità": 10}

    response = await client.put(
        f"/ordini/ordinearticolo/{order.id}", headers=headers, json=payload
    )

    assert response.status_code == 200


@pytest.mark.anyio
async def test_rimuovi_articolo_ordine(client, user_token, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    result = await db_session.execute(
        select(User).where(User.email == "mario.rossi@gmail.com")
    )
    user = result.scalar_one_or_none()

    order = await CreateOrderSetup.create_order(
        db=db_session, user=user, articolo=articolo
    )

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.delete(
        f"/ordini/articolo/{order.id}/{articolo.id}", headers=headers
    )

    assert response.status_code == 200


@pytest.mark.anyio
async def test_rimuovi_ordine(client, user_token, db_session):
    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    result = await db_session.execute(
        select(User).where(User.email == "mario.rossi@gmail.com")
    )
    user = result.scalar_one_or_none()

    order = await CreateOrderSetup.create_order(
        db=db_session, user=user, articolo=articolo
    )

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.delete(f"/ordini/delete/{order.id}", headers=headers)

    assert response.status_code == 200
