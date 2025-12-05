from pydantic import BaseModel, Field

from app.schemas.user import UserOut


class DoctorBase(BaseModel):
    crm: str = Field(
        ..., pattern=r'^\d{10}$', description='CRM must contain 10 digits'
    )


class DoctorIn(DoctorBase):
    cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )


class DoctorOut(DoctorBase):
    user: UserOut


class DoctorUpdate(BaseModel):
    crm: str | None = None
