from pydantic import BaseModel, Field


class VaccineBase(BaseModel):
    patient_cpf: str = Field(..., pattern=r'^\d{11}$')
    nurse_cpf: str = Field(..., pattern=r'^\d{11}$')
    name: str
    description: str
    manufacturer: str


class VaccineIn(VaccineBase):
    pass

class VaccineOut(VaccineBase):
    id: int


class VaccineUpdate(VaccineBase):
    pass