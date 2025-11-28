from datetime import datetime
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    relationship,
    validates,
)

from app.enums import UserRole
from app.utils import hash_password, sanitizar_name

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    stores_owned: Mapped[list["Store"]] = relationship(back_populates="partner")
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.CLIENT
    )

    @validates('username')
    def validar_username(self, key, name: str) -> str:  # noqa: PLR6301
        return sanitizar_name(name)

    @validates('senha')
    def validar_senha(self, key, password: str) -> str:  # noqa: PLR6301
        return hash_password(password)


@table_registry.mapped_as_dataclass
class StoreFoodTypes:
    __tablename__ = "store_food_types"
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), primary_key=True)
    food_type_id: Mapped[int] = mapped_column(ForeignKey("food_types.id"), primary_key=True)


@table_registry.mapped_as_dataclass
class FoodTypeModel:
    __tablename__ = "food_types"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    stores: Mapped[list["Store"]] = relationship(
        secondary="store_food_types",
        back_populates="food_types"
    )


@table_registry.mapped_as_dataclass
class Store:
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    address: Mapped[str]
    partner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )
    food_types: Mapped[list["FoodTypeModel"]] = relationship(
        secondary="store_food_types",
        back_populates="stores"
    )
    partner: Mapped[User] = relationship(back_populates="stores_owned")


