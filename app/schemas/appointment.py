from datetime import datetime

from pydantic import BaseModel, EmailStr


class AppointmentBase(BaseModel):
    doctor_cpf: str
    patient_cpf: str
    ubs_cnes: str
    date: datetime


class AppointmentIn(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    message : str
    
