from datetime import datetime

from pydantic import BaseModel


class PrescriptionBase(BaseModel):
    doctor_cpf: str
    patient_cpf: str
    ubs_cnes: str
    date: datetime
    description: str
    date: datetime


class PrescriptionIn(PrescriptionBase):
    pass


class PrescriptionOut(PrescriptionBase):
    message: str


class PrescriptionUpdate(BaseModel):
    doctor_cpf: str | None = None
    patient_cpf: str | None = None
    ubs_cnes: str | None = None
    date: datetime | None = None
    description: str | None = None
    date: datetime | None = None
