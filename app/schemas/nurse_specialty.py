from pydantic import BaseModel, Field  


class Nurse_specialtyBase(BaseModel):
    nurse_cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    speciality: str
    

class Nurse_specialtyIn(Nurse_specialtyBase):
    pass


class Nurse_specialtyOut(Nurse_specialtyBase):
    message : str

class Nurse_specialtyUpdate(BaseModel):
    nurse_cpf: str | None = None
    speciality: str | None = None
    
