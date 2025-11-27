from datetime import date

from sqlalchemy import ForeignKey, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.appointment import Appointment
from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Prescription:
    __tablename__ = "prescription"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointment.id"))
    description: Mapped[str] = mapped_column(String(200))

    appointment: Mapped[Appointment] = relationship("Appointment")
