from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Specialty:
    __tablename__ = 'specialty'

    code: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
