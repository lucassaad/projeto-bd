from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.registry import table_registry
from app.models.user import User


@table_registry.mapped_as_dataclass
class Patient:
    __tablename__ = 'patient'

    cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('user.cpf'), primary_key=True
    )

    user: Mapped[User] = relationship('User')
