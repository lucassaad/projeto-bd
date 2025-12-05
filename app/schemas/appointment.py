from datetime import datetime

from pydantic import BaseModel, Field


class AppointmentBase(BaseModel):
    doctor_cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    patient_cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    ubs_cnes: str
    date: datetime


class AppointmentIn(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int | None = None
    pass


class AppointmentUpdate(AppointmentBase):
    doctor_cpf: str | None = None
    patient_cpf: str | None = None
    ubs_cnes: str | None = None
    date: datetime | None = None
