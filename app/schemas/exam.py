from datetime import datetime

from pydantic import BaseModel   


class examBase(BaseModel):
    type: str
    date_appointment: datetime
    doctor_cpf: str
    patient_cpf: str
    cnes_ubs: str


class ExamIn(examBase):
    pass


class ExamOut(examBase):
    pass


class ExamUpdate(BaseModel):
    type: str | None = None
    date_appointment: datetime | None = None
    doctor_cpf: str | None = None
    patient_cpf: str | None = None
    cnes_ubs: str | None = None
