from pydantic import BaseModel, Field

from app.schemas.user import UserOut


class PatientBase(BaseModel):
    cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )


class PatientIn(PatientBase):
    pass


class PatientOut(PatientBase):
    user: UserOut


class PatientUpdate(BaseModel):
    cpf: str | None = None
