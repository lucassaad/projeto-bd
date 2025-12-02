from pydantic import BaseModel, Field

class PatientBase(BaseModel):
    cpf : str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )


class PatientIn(PatientBase):
    pass


class PatientOut(PatientBase):
    pass

class PatientUpdate(PatientBase):
    cpf : str | None = None
