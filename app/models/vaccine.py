from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.nurse import Nurse
from app.models.patient import Patient
from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Vaccine:
    __tablename__ = 'vaccine'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    patient_cpf: Mapped[int] = mapped_column(
        String(11), ForeignKey('patient.cpf')
    )
    nurse_cpf: Mapped[str] = mapped_column(String(11), ForeignKey('nurse.cpf'))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))
    manufacturer: Mapped[str] = mapped_column(String(100))

    patient: Mapped[Patient] = relationship('Patient')
    nurse: Mapped[Nurse] = relationship('Nurse')
