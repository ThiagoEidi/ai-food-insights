from sqlalchemy.orm import Mapped, mapped_column, registry, validates

from app.utils import sanitizar_name

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]

    @validates('username')
    def validar_username(self, key, name: str) -> str:  # noqa: PLR6301
        return sanitizar_name(name)

    @validates('senha')
    def validar_senha(self, key, plain_password: str) -> str:
        if len(plain_password) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        return hash_password(plain_password) 
