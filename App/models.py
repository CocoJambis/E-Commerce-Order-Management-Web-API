from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import String, Integer, Float, ForeignKey

Base = declarative_base()


class OrderArticolo(Base):
    __tablename__ = "order_detail"

    order_id : Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    articolo_id : Mapped[int] = mapped_column(ForeignKey("articoli.id", ondelete="RESTRICT"), nullable=False, primary_key=True)
    quantità_ordinata : Mapped[int] = mapped_column(Integer, nullable=False)

    order : Mapped["Order"] = relationship(back_populates="dettagli_articoli")
    articolo : Mapped["Articolo"] = relationship()

class User(Base):
    __tablename__ = "users"


    id : Mapped[int] = mapped_column(primary_key=True)
    first_name : Mapped[str] = mapped_column(String, nullable=False)
    last_name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, nullable=False, unique=True)

    orders : Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Articolo(Base):
    __tablename__ = "articoli"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    desc : Mapped[str] = mapped_column(String, nullable=False)
    prezzo : Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quantità : Mapped[int] = mapped_column(Integer, nullable=False, default=0)



class Order(Base):
    __tablename__ = "orders"

    id : Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    user : Mapped["User"] = relationship(back_populates="orders")
    dettagli_articoli : Mapped[List["OrderArticolo"]] = relationship(back_populates="order", cascade="all, delete-orphan")
