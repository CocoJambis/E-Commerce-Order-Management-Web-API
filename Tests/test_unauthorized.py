import pytest


@pytest.mark.anyio
async def test_create_product_unauthorized(client):

    payload = {
        "name" : "test",
        "desc" : "test",
        "prezzo" : 20,
        "quantità" : 20
    }

    response = await client.post("/admin/articolo", json=payload)

    assert response.status_code == 401


@pytest.mark.anyio
async def test_modifica_prezzo_articolo(client):

    payload = {
        "prezzo" : 20
    }

    response = await client.put("/admin/1", json=payload)

    assert response.status_code == 401

@pytest.mark.anyio
async def test_aggiungi_giacenza_articolo(client):

    payload = {
        "quantità" : 20
    }

    response = await client.put("/admin/aggiungigiacenza/1", json=payload)

    assert response.status_code == 401


@pytest.mark.anyio
async def test_elimina_articolo(client):

    response = await client.delete("/admin/articolo/1")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_all_users(client):

    response = await client.get("/admin/users")

    assert response.status_code == 401

@pytest.mark.anyio
async def test_elimina_utente(client):

    response = await client.delete("/admin/user/1")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_tutti_gli_ordini(client):

    response = await client.get("/admin/orders")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_lista_articoli_ordinati(client):

    response = await client.get("/admin/articoliordinati/1")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_delete_order(client):

    response = await client.delete("/admin/orders/1")

    assert response.status_code == 401