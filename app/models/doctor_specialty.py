from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.doctor import Doctor
from app.models.registry import table_registry
from app.models.specialty import Specialty


@table_registry.mapped_as_dataclass
class Doctor_Specialty:
    __tablename__ = 'doctor_specialty'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    doctor_cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('doctor.cpf')
    )
    specialty_code: Mapped[int] = mapped_column(ForeignKey('specialty.code'))

    doctor: Mapped[Doctor] = relationship('Doctor')
    specialty: Mapped[Specialty] = relationship('Specialty')
