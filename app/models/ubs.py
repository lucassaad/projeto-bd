from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Ubs:
    __tablename__ = 'ubs'

    cnes: Mapped[str] = mapped_column(String(7), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    addres: Mapped[str] = mapped_column(String(200))
