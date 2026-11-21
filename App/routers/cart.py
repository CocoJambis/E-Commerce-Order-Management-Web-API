from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from App.db import get_session
from App.models import User, OrderArt, ArticoloCart, CartOut
from App.crud import get_current_active_user, CartRepository

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/{user_id}/items", response_model=ArticoloCart)
async def add_to_cart(
    payload: OrderArt,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
):
    return await CartRepository.add_to_cart(
        payload=payload, current_user=current_user, db=db
    )


@router.get("/{user_id}", response_model=CartOut)
async def view_cart(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
):
    return await CartRepository.view_cart(current_user=current_user, db=db)


@router.put("/{item_id}", response_model=CartOut)
async def remove_quantity_from_product(
    item_id: int,
    quantity: int | None = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
):
    return await CartRepository.remove_item_from_cart(
        db=db, item_id=item_id, current_user=current_user, quantity=quantity
    )
