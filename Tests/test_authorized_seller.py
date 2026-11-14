import pytest
from httpx import AsyncClient


class Seller:
    @staticmethod
    async def seller_payload():

        return {
            "first_name": "mario",
            "last_name": "rossi",
            "email": "mario.rossi@gmail.com",
            "password": "123",
        }

    @staticmethod
    async def create_user_seller(client: AsyncClient) -> str:

        payload = await Seller.seller_payload()

        await client.post("/seller/register/seller", json=payload)

        login_payload = {"username": "mario.rossi@gmail.com", "password": "123"}

        response = await client.post("/users/token", data=login_payload)

        token = response.json()["access_token"]

        return token


@pytest.mark.anyio
async def test_register_seller(client):

    payload = await Seller.seller_payload()

    response = await client.post("/seller/register/seller", json=payload)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_sell_article(client):

    token = await Seller.create_user_seller(client)

    headers = {"Authorization": f"Bearer {token}"}

    articolo_payload = {"name": "test", "desc": "test", "prezzo": 20, "quantità": 20}

    response_sell = await client.post(
        "/seller/sell", headers=headers, json=articolo_payload
    )

    assert response_sell.status_code == 200


@pytest.mark.anyio
async def test_get_articles(client):

    token = await Seller.create_user_seller(client)

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/seller/articles", headers=headers)

    assert response.status_code == 200
