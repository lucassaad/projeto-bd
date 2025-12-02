from pydantic import BaseModel   


class UbsBase(BaseModel):
    cnes: str
    name : str
    address: str

class UbsIn(UbsBase):
    pass


class UbsOut(UbsBase):
    message : str


class UbsUpdate(UbsBase):
    cnes: str | None = None
    name : str | None = None
    address: str | None = None
    
