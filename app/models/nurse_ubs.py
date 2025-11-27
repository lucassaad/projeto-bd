from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.nurse import Nurse
from app.models.registry import table_registry
from app.models.ubs import Ubs


@table_registry.mapped_as_dataclass
class Nurse_Ubs:
    __tablename__ = 'nurse_ubs'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    nurse_cpf: Mapped[str] = mapped_column(
        String(11), ForeignKey('nurse.cpf')
    )
    ubs_cnes: Mapped[str] = mapped_column(String(7), ForeignKey('ubs.cnes'))

    nurse: Mapped[Nurse] = relationship('Nurse')
    ubs: Mapped[Ubs] = relationship('Ubs')
