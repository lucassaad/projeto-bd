from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.registry import table_registry
from app.models.user import User


@table_registry.mapped_as_dataclass
class Nurse:
    __tablename__ = 'nurse'

    cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('user.cpf'), primary_key=True
    )
    coren: Mapped[str] = mapped_column(String(9), unique=True)

    user: Mapped[User] = relationship('User')
