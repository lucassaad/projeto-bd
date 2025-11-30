from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    name: str
    phone_number: str = Field(..., pattern=r'^\d{10,11}$')
    birthdate: date
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    pass


class UserUpdate(UserBase):
    password: str
