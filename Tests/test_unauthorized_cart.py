import pytest


@pytest.mark.anyio
async def test_add_to_cart(client):
    payload = {
        "articolo_id" : 12,
        "quantità" : 2
    }

    response = await client.post("/cart/1/items", json=payload)

    assert response.status_code == 401

@pytest.mark.anyio
async def test_view_cart(client):

    response = await client.get("/cart/1")

    assert response.status_code == 401

@pytest.mark.anyio
async def test_remove_quantity_from_product(client):

    payload = {
        "item_id" : 1,
        "quantity" : 1
    }

    response = await client.put("/cart/1", json= payload)

    assert response.status_code == 401