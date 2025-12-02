from datetime import datetime

from pydantic import BaseModel   


class Medication_preBase(BaseModel):
    anvisa_code : str
    date : datetime
    patient_cpf : str
    nurse_cpf : str
    cnes_ubs : str


class Medication_preIn(Medication_preBase):
    pass


class Medication_preOut(Medication_preBase):
    pass


class Medication_preUpdate(Medication_preBase):
    anvisa_code : str | None = None
    date : datetime | None = None
    patient_cpf : str | None = None
    nurse_cpf : str | None = None
    cnes_ubs : str | None = None
    
