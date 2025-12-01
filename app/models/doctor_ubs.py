from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.doctor import Doctor
from app.models.registry import table_registry
from app.models.ubs import Ubs


@table_registry.mapped_as_dataclass
class Doctor_Ubs:
    __tablename__ = 'doctor_ubs'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    doctor_cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('doctor.cpf')
    )
    ubs_cnes: Mapped[str] = mapped_column(String(7), ForeignKey('ubs.cnes'))

    doctor: Mapped[Doctor] = relationship('Doctor')
    ubs: Mapped[Ubs] = relationship('Ubs')
