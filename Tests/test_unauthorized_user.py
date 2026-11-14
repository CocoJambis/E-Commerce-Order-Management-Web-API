import pytest


@pytest.mark.anyio
async def test_get_orders(client):

    response = await client.get("/users/orders")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_order_details(client):

    response = await client.get("/users/orders/details/1")

    assert response.status_code == 401
