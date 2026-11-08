import pytest


@pytest.mark.anyio
async def test_register_user_success(client):

    payload = {
        "first_name" : "mario",
        "last_name" : "rossi",
        "email" : "mario.rossi@gmail.com",
        "password" : "123"
    }

    response = await client.post("/users/register", json=payload)


    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "mario.rossi@gmail.com"
    assert data["first_name"] == "mario"
    assert data["last_name"] == "rossi"
    assert "password" not in data


@pytest.mark.anyio
async def test_login_success(client):

    payload = {
        "first_name" : "mario",
        "last_name" : "rossi",
        "email" : "mario.rossi@gmail.com",
        "password" : "123"
    }

    await client.post("/users/register", json=payload)

    login_payload = {
        "username" : "mario.rossi@gmail.com",
        "password" : "123"
    }

    response = await client.post("/users/token", data=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_wrong_password(client):

    payload = {
        "first_name" : "mario",
        "last_name" : "rossi",
        "email" : "mario.rossi@gmail.com",
        "password" : "123"
    }

    await client.post("/users/register", json=payload)

    login_payload = {
        "username" : "mario.rossi@gmail.com",
        "password" : "2123"
    }

    response = await client.post("/users/token", data=login_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Username o password errati!"


@pytest.mark.anyio
async def test_token_access(client):

    register_payload = {
        "first_name" : "mario",
        "last_name" : "rossi",
        "email" : "mario.rossi@gmail.com",
        "password" : "123"
}

    await client.post("/users/register", json=register_payload)

    login_payload = {
        "username" : "mario.rossi@gmail.com",
        "password" : "123"
    }

    response = await client.post("/users/token", data=login_payload)
    token = response.json()["access_token"]


    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/users/orders", headers=headers)

    assert response.status_code == 200



