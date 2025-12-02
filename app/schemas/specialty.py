from pydantic import BaseModel, Field

class SpecialtyBase(BaseModel):
    name: str


class SpecialtyIn(SpecialtyBase):
    pass


class SpecialtyOut(SpecialtyBase):
    code: int

class SpecialtyUpdate(BaseModel):
    pass
