from pydantic import BaseModel   


class UbsBase(BaseModel):
    cnes: str
    name : str
    address: str

class UbsIn(ubsBase):
    pass


class UbsOut(ubsBase):
    message : str


class UbsUpdate(ubsBase):
    cnes: str | None = None
    name : str | None = None
    address: str | None = None
    
