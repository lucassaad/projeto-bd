from pydantic import BaseModel   


class ubsBase(BaseModel):
    cnes: str
    name : str
    address: str

class ubsIn(ubsBase):
    pass


class ubsOut(ubsBase):
    message : str


class ubsUpdate(ubsBase):
    cnes: str | None = None
    name : str | None = None
    address: str | None = None
    
