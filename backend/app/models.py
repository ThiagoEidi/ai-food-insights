from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    relationship,
    validates,
)

from app.utils import hash_password, sanitizar_name

table_registry = registry()


class UserRole(Enum):
    CLIENT = 'client'
    PARTNER = 'partner'
    ADMIN = 'admin'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]

    stores_owned: Mapped[list['Store']] = relationship(
        back_populates='partner',
        default_factory=list,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.CLIENT,
    )

    @validates('username')
    def validar_username(self, key, name: str) -> str:  # noqa: PLR6301
        return sanitizar_name(name)

    @validates('senha')
    def validar_senha(self, key, password: str) -> str:  # noqa: PLR6301
        return hash_password(password)


@table_registry.mapped_as_dataclass
class StoreFoodTypes:
    __tablename__ = 'store_food_types'

    store_id: Mapped[int] = mapped_column(
        ForeignKey('stores.id'), primary_key=True, init=False
    )

    food_type_id: Mapped[int] = mapped_column(
        ForeignKey('food_types.id'), primary_key=True
    )

    store: Mapped['Store'] = relationship(
        back_populates='food_type_associations', init=False
    )
    food_type: Mapped['FoodTypeModel'] = relationship(
        back_populates='store_associations', init=False
    )


@table_registry.mapped_as_dataclass
class FoodTypeModel:
    __tablename__ = 'food_types'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    store_associations: Mapped[list['StoreFoodTypes']] = relationship(
        back_populates='food_type', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Store:
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    address: Mapped[str]

    partner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    food_type_associations: Mapped[list['StoreFoodTypes']] = relationship(
        back_populates='store', cascade='all, delete-orphan'
    )

    partner: Mapped[User] = relationship(back_populates='stores_owned', init=False)
