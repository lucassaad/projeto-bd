from pydantic import BaseModel


class SpecialtyBase(BaseModel):
    name: str


class SpecialtyIn(SpecialtyBase):
    pass


class SpecialtyOut(SpecialtyBase):
    code: int


class SpecialtyUpdate(BaseModel):
    pass
