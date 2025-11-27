from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.patient import Patient
from app.models.registry import table_registry
from app.models.ubs import Ubs


@table_registry.mapped_as_dataclass
class Patient_Ubs:
    __tablename__ = 'patient_ubs'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    patient_cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('patient.cpf')
    )
    ubs_cnes: Mapped[str] = mapped_column(String(7), ForeignKey('ubs.cnes'))

    patient: Mapped[Patient] = relationship('Patient')
    ubs: Mapped[Ubs] = relationship('Ubs')
