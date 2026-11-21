from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from decimal import Decimal
from App.models import CategoriaArticolo


# User Models
class UserCreate(BaseModel):
    first_name: str = Field(min_length=3, max_length=20)
    last_name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)


# Articolo Models
class ArticoloCreate(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    desc: str = Field(min_length=5, max_length=20)
    prezzo: float
    quantità: int
    category: CategoriaArticolo


class ArticoloResponse(BaseModel):
    id: int
    name: str
    desc: str
    prezzo: float
    quantità: int
    seller_id: int
    seller_name: str
    category: CategoriaArticolo

    model_config = ConfigDict(from_attributes=True)


class ArticoloCart(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    prezzo: float
    subtotal: Decimal
    name: str
    seller_name: str

    model_config = ConfigDict(from_attributes=True)


class CartOut(BaseModel):
    id: int
    user_id: int
    items: list[ArticoloCart]
    total_amount: Decimal

    model_config = ConfigDict(from_attributes=True)


class ModificaPrezzoArticolo(BaseModel):
    prezzo: float


class ModificaGiacenzaArticolo(BaseModel):
    quantità: int


# Order Models
class OrderArt(BaseModel):
    articolo_id: int
    quantità: int = Field(gt=0)


class OrderCreate(BaseModel):
    articoli: list[OrderArt]


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: float

    model_config = ConfigDict(from_attributes=True)


# OrderArticolo models
class ArticoliOrdinati(BaseModel):
    order_id: int
    articolo_id: int
    quantità_ordinata: int

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
