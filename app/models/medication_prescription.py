from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.medication import Medication
from app.models.prescription import Prescription
from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Medication_Prescription:
    __tablename__ = 'medication_prescription'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )

    medication_code: Mapped[str] = mapped_column(
        String(13), ForeignKey('medication.anvisa_code')
    )
    prescription_id: Mapped[int] = mapped_column(ForeignKey('prescription.id'))

    medication: Mapped[Medication] = relationship('Medication')
    prescription: Mapped[Prescription] = relationship('Prescription')
