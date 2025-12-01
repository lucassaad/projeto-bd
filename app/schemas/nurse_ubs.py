from pydantic import BaseModel   


class Nurse_ubsBase(BaseModel):
    nurse_cpf: str
    ubs_cnes: str
    

class Nurse_ubsIn(Nurse_ubsBase):
    pass


class Nurse_ubsOut(Nurse_ubsBase):
    message : str

class Nurse_ubsUpdate(Nurse_ubsBase):
    nurse_cpf: str | None = None
    ubs_cnes: str | None = None
    
