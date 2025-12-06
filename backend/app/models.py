from typing import List

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)

from app.enums import OrderStatus
from app.utils import hash_password, sanitizar_name


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type',
    }

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]

    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(256), nullable=False)

    @validates('senha')
    def validate_password(self, key, value: str) -> str:  # noqa: PLR6301
        return hash_password(value)


class Client(User):
    __tablename__ = 'clients'
    __mapper_args__ = {'polymorphic_identity': 'client'}

    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    orders: Mapped[List['Order']] = relationship(back_populates='client')

    @validates('username')
    def validate_username(self, key, value: str) -> str:  # noqa: PLR6301
        return sanitizar_name(value)


class Admin(User):
    __tablename__ = 'admins'
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)


class Partner(User):
    __tablename__ = 'partners'
    __mapper_args__ = {'polymorphic_identity': 'partner'}

    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    name: Mapped[str]
    address: Mapped[str]

    categories: Mapped[List['PartnerFoodTypes']] = relationship(
        back_populates='partner', cascade='all, delete-orphan'
    )
    items: Mapped[List['Item']] = relationship(
        back_populates='partner', cascade='all, delete-orphan'
    )
    orders: Mapped[List['Order']] = relationship(back_populates='partner_restaurant')


class PartnerFoodTypes(Base):
    __tablename__ = 'partner_food_types'

    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id'), primary_key=True)
    food_type_id: Mapped[int] = mapped_column(
        ForeignKey('food_types.id'), primary_key=True
    )

    partner: Mapped['Partner'] = relationship(back_populates='categories')
    food_type: Mapped['FoodType'] = relationship(back_populates='partner_associations')


class FoodType(Base):
    __tablename__ = 'food_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    partner_associations: Mapped[List['PartnerFoodTypes']] = relationship(
        back_populates='food_type', cascade='all, delete-orphan'
    )


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    description: Mapped[str | None]

    order_items: Mapped[List['OrderItem']] = relationship(
        back_populates='item', cascade='all, delete-orphan'
    )

    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id'))
    partner: Mapped['Partner'] = relationship(back_populates='items')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id'))

    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)
    total: Mapped[float]
    client: Mapped['Client'] = relationship(back_populates='orders')
    partner_restaurant: Mapped['Partner'] = relationship(back_populates='orders')

    items: Mapped[List['OrderItem']] = relationship(
        back_populates='order', cascade='all, delete-orphan'
    )
 

class OrderItem(Base):
    __tablename__ = 'order_items'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), primary_key=True)

    quantity: Mapped[int]
    price_at_purchase: Mapped[float]

    order: Mapped['Order'] = relationship(back_populates='items')
    item: Mapped['Item'] = relationship(back_populates='order_items')
