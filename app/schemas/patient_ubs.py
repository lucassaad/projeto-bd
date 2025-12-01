from pydantic import BaseModel   


class Patient_ubsBase(BaseModel):
    patient_cpf: str
    ubs_cnes: str
    

class Patient_ubsIn(Patient_ubsBase):
    pass


class Nurse_ubsOut(Patient_ubsBase):
    message : str

class Nurse_ubsUpdate(Patient_ubsBase):
    patient_cpf: str | None = None
    ubs_cnes: str | None = None
    
    
