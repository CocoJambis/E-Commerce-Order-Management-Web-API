import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from App.models import User, Cart, CartItem
from Tests.conftest import CreateOrderSetup

@pytest.mark.anyio
async def test_add_to_cart(client, user_token, db_session):

    token = user_token

    headers = {"Authorization" : f"Bearer {token}"}

    result = await db_session.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()

    articolo = await CreateOrderSetup.create_article(
        seller= user,
        db= db_session
    )

    payload = {
        "articolo_id" : articolo.id,
        "quantità" : 1
    }

    response = await client.post("/cart/1/items", json=payload, headers=headers)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_view_cart(client, user_token, db_session):

    token = user_token

    headers = {"Authorization" : f"Bearer {token}"}

    result = await db_session.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()

    response = await client.get(f"/cart/{user.id}", headers= headers)

    assert response.status_code == 200

@pytest.mark.anyio
async def test_remove_quantity_from_cart(client, user_token, db_session):

    token = user_token

    headers = {"Authorization" : f"Bearer {token}"}

    result = await db_session.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()

    articolo = await CreateOrderSetup.create_article(
        seller= user,
        db= db_session
    )

    payload = {
        "articolo_id" : articolo.id,
        "quantità" : 1
    }

    response_cart = await client.post("/cart/1/items", json= payload, headers= headers)

    assert response_cart.status_code == 200

    result_cart = await db_session.execute(select(Cart)
                                            .options(selectinload(Cart.items)
                                            .selectinload(CartItem.product)).where(Cart.user_id == 1))
                                            
    cart = result_cart.scalar_one_or_none()

    response_remove_quantity = await client.put(f"/cart/{articolo.id}?quantity=1", headers= headers)

    assert response_remove_quantity.status_code == 200

    db_session.expire_all()

    result_cart = await db_session.execute(
        select(Cart)
        .options(selectinload(Cart.items))
        .where(Cart.user_id == 1)
    )

    cart = result_cart.scalar_one_or_none()

    assert cart is not None
    assert len(cart.items) == 0






