from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.registry import table_registry
from app.models.user import User


@table_registry.mapped_as_dataclass
class Doctor:
    __tablename__ = 'doctor'

    cpf: Mapped[str] = mapped_column(ForeignKey('user.cpf'), primary_key=True)
    crm: Mapped[str] = mapped_column(String(10), unique=True)

    user: Mapped[User] = relationship('User')
