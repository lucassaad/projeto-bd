from pydantic import BaseModel   


class Nurse_specialityBase(BaseModel):
    nurse_cpf: str
    type: str
    

class Nurse_specialityIn(Nurse_specialityBase):
    pass


class Nurse_specialityOut(Nurse_specialityBase):
    message : str

class Nurse_specialityUpdate(Nurse_specialityBase):
    nurse_cpf: str | None = None
    type: str | None = None
    
