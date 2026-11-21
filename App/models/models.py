import enum
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import (
    String,
    Integer,
    Float,
    ForeignKey,
    Boolean,
    Enum as SQLEnum,
    UniqueConstraint,
    CheckConstraint,
)

Base = declarative_base()


class CategoriaArticolo(str, enum.Enum):
    ELETTRONICA = "elettronica"
    ABBIGLIAMENTO = "abbigliamento"
    CASA = "casa"
    LIBRI = "libri"
    ELETTRODOMESTICI = "elettrodomestici"
    AUTO = "auto"
    MOTO = "moto"
    IGIENE = "igiene"
    CANE = "cane"
    GATTO = "gatto"
    ANIMALI_DOMESTICI = "animali domestici"


class OrderArticolo(Base):
    __tablename__ = "order_detail"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    articolo_id: Mapped[int] = mapped_column(
        ForeignKey("articoli.id", ondelete="RESTRICT"), nullable=False, primary_key=True
    )
    quantità_ordinata: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["Order"] = relationship(back_populates="dettagli_articoli")
    articolo: Mapped["Articolo"] = relationship()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_pwd: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, default="User", nullable=False)

    orders: Mapped[List["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    articoli_venduti: Mapped[List["Articolo"]] = relationship(
        back_populates="seller", cascade="all, delete-orphan"
    )

    cart: Mapped["Cart"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user_email: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship(back_populates="cart")
    items: Mapped[List["CartItem"]] = relationship(
        back_populates="cart", cascade="all, delete-orphan"
    )

    @hybrid_property
    def total_amount(self) -> Decimal:
        if not self.items:
            return Decimal("0.00")
        return sum((item.subtotal for item in self.items), Decimal("0.00"))


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("articoli.id", ondelete="CASCADE")
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    prezzo: Mapped[float] = mapped_column(Float, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    seller_name: Mapped[str] = mapped_column(String, nullable=False)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Articolo"] = relationship()

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
        CheckConstraint("quantity > 0", name="ck_cart_item_quantity_positive"),
    )

    @hybrid_property
    def subtotal(self) -> Decimal:
        return Decimal(str(self.prezzo)) * self.quantity


class Articolo(Base):
    __tablename__ = "articoli"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    desc: Mapped[str] = mapped_column(String, nullable=False)
    prezzo: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quantità: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category: Mapped[CategoriaArticolo] = mapped_column(
        SQLEnum(CategoriaArticolo, native_enum=False),
        nullable=False,
        default="elettronica",
    )
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    seller_name: Mapped[str] = mapped_column(String, nullable=False)

    seller: Mapped["User"] = relationship(back_populates="articoli_venduti")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    user: Mapped["User"] = relationship(back_populates="orders")
    dettagli_articoli: Mapped[List["OrderArticolo"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
