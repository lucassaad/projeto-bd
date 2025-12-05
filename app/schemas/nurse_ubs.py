from pydantic import BaseModel, Field


class Nurse_ubsBase(BaseModel):
    nurse_cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    ubs_cnes: str


class Nurse_ubsIn(Nurse_ubsBase):
    pass


class Nurse_ubsOut(Nurse_ubsBase):
    message: str


class Nurse_ubsUpdate(BaseModel):
    nurse_cpf: str | None = None
    ubs_cnes: str | None = None
