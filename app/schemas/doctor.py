from pydantic import BaseModel, Field


class DoctorBase(BaseModel):
    cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    crm: str


class DoctorIn(DoctorBase):
    pass

class DoctorOut(DoctorBase):
    id: int | None = None   
    pass

class DoctorUpdate(DoctorBase):
    name: str | None = None
    crm: str | None = None