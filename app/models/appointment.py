from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.registry import table_registry
from app.models.ubs import Ubs


@table_registry.mapped_as_dataclass
class Appointment:
    __tablename__ = 'appointment'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    doctor_cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('doctor.cpf')
    )
    patient_cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('patient.cpf')
    )
    ubs_cnes: Mapped[str] = mapped_column(String(7), ForeignKey('ubs.cnes'))

    doctor: Mapped[Doctor] = relationship('Doctor')
    patient: Mapped[Patient] = relationship('Patient')
    ubs: Mapped[Ubs] = relationship('Ubs')

    appointment_datetime: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
