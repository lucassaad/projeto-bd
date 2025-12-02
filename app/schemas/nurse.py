from pydantic import BaseModel, Field

from app.schemas.user import UserOut


class NurseBase(BaseModel):
    coren : str = Field(
        ..., pattern=r'^\d{9}$', description='Coren must contain 9 digits'
    )


class NurseIn(NurseBase):
    cpf : str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )

class NurseOut(NurseBase):
    user: UserOut

class NurseUpdate(BaseModel):
    coren: str | None = None