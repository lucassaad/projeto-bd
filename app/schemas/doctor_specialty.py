from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class DoctorSpecialtyBase(BaseModel):
    doctor_cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    specialty_code: int


class DoctorSpecialtyIn(DoctorSpecialtyBase):
    pass


class DoctorSpecialtyOut(DoctorSpecialtyBase):
    id: int | None = None  
    pass
    
