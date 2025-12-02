from pydantic import BaseModel   


class vaccineBase(BaseModel):
    anvisa_code: str
    manufacturer: str
    description: str
    patient_cpf: str
    nurse_cpf: str


class VaccineIn(vaccineBase):
    pass


class VaccineOut(vaccineBase):
    message : str


class VaccineUpdate(vaccineBase):
    anvisa_code: str | None = None
    manufacturer: str | None = None
    description: str | None = None
    patient_cpf: str | None = None
    nurse_cpf: str | None = None
    
