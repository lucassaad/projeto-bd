from pydantic import BaseModel, Field


class NurseBase(BaseModel):
    cpf : str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    coren: str


class NurseIn(NurseBase):
    pass

class NurseOut(NurseBase):
    pass

class NurseUpdate(NurseBase):
    name: str | None = None
    coren: str | None = None