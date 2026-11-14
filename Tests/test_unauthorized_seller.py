import pytest


@pytest.mark.anyio
async def test_sell(client, user_token):

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    payload = {"name": "test", "desc": "test", "prezzo": 20, "quantità": 20}

    response = await client.post("/seller/sell", headers=headers, json=payload)

    assert response.status_code == 401


@pytest.mark.anyio
async def test_list_sell(client, user_token):

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/seller/articles", headers=headers)

    assert response.status_code == 401
