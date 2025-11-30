from datetime import date

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    cpf: str
    name: str
    phone_number: str
    birthdate: date
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass
