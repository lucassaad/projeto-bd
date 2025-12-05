from datetime import date

from sqlalchemy import Date, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(11))
    birthdate: Mapped[date] = mapped_column(Date())
    email: Mapped[str] = mapped_column(String(254))
    password: Mapped[str] = mapped_column(
        String(64)
    )  # sha256 returns 256 bits == 64 hex characters
    image: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
