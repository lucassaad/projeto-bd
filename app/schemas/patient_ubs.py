from pydantic import BaseModel, Field  


class Patient_ubsBase(BaseModel):
    patient_cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    ubs_cnes: str
    

class Patient_ubsIn(Patient_ubsBase):
    pass
    
class Patient_ubsOut(Patient_ubsBase):
    message : str

class Patient_ubsUpdate(Patient_ubsBase):
    patient_cpf: str | None = None
    ubs_cnes: str | None = None
    
    
