import pytest
from Tests.conftest import CreateOrderSetup
from sqlalchemy import select
from App.models import User


@pytest.mark.anyio
async def test_lista_user_orders(client, user_token):

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/users/orders", headers=headers)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_dettagli_ordine(client, user_token, db_session):

    seller = await CreateOrderSetup.create_seller(db_session)
    articolo = await CreateOrderSetup.create_article(seller=seller, db=db_session)

    rs = await db_session.execute(
        select(User).where(User.email == "mario.rossi@gmail.com")
    )
    user = rs.scalar_one_or_none()

    await CreateOrderSetup.create_order(
        db=db_session, user=user, articolo=articolo
    )

    token = user_token

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/users/orders/details/1", headers=headers)

    assert response.status_code == 200, f"Errore : {response.text}"
