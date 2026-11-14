import pytest
from Tests.conftest import Payloads, CreateOrderSetup


@pytest.mark.anyio
async def test_create_articolo_admin(client, admin_token: str):

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    json = await Payloads.articolo_payload()

    response = await client.post("/admin/articolo", headers=headers, json=json)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_modifica_articolo(client, admin_token: str, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    payload = {"prezzo": 20}

    response = await client.put(f"admin/{articolo.id}", headers=headers, json=payload)

    assert response.status_code == 200
    assert articolo.prezzo == 20


@pytest.mark.anyio
async def test_aggiungi_giacenza_articolo(client, admin_token: str, db_session):

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    payload = {"quantità": 20}

    response = await client.put(
        f"/admin/aggiungigiacenza/{articolo.id}", headers=headers, json=payload
    )

    assert response.status_code == 200
    assert articolo.quantità == 40


@pytest.mark.anyio
async def test_delete_articolo(client, admin_token, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    assert articolo.id == 1

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.delete(f"/admin/articolo/{articolo.id}", headers=headers)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_users_list(client, admin_token):

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/admin/users", headers=headers)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_delete_user(client, admin_token):

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.delete("/admin/user/1", headers=headers)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_all_orders(client, admin_token):

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/admin/orders", headers=headers)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_articoli_ordinati(client, admin_token, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)
    order = await CreateOrderSetup.create_order(
        db=db_session, user=seller, articolo=articolo
    )

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get(f"/admin/articoliordinati/{order.id}", headers=headers)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_delete_order(client, admin_token, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)
    order = await CreateOrderSetup.create_order(
        db=db_session, user=seller, articolo=articolo
    )

    token = admin_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.delete(f"/admin/orders/{order.id}", headers=headers)

    assert response.status_code == 200
