from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.nurse import Nurse
from app.models.registry import table_registry
from app.models.specialty import Specialty


@table_registry.mapped_as_dataclass
class Nurse_Specialty:
    __tablename__ = 'nurse_specialty'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    nurse_cpf: Mapped[str] = mapped_column(String(11), ForeignKey('nurse.cpf'))
    specialty_code: Mapped[int] = mapped_column(ForeignKey('specialty.code'))

    nurse: Mapped[Nurse] = relationship('Nurse')
    specialty: Mapped[Specialty] = relationship('Specialty')
