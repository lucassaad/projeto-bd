from pydantic import BaseModel, Field


class UbsBase(BaseModel):
    cnes: str = Field(..., pattern=r'^\d{7}$')
    name: str
    addres: str


class UbsIn(UbsBase):
    pass


class UbsOut(UbsBase):
    pass 

class UbsUpdate(UbsBase):
    pass
