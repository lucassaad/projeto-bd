from datetime import datetime

from pydantic import BaseModel   


class MedicationBase(BaseModel):
    anvisa_code: str
    name : str
    description : str


class MedicationIn(MedicationBase):
    pass


class MedicationOut(MedicationBase):
    pass


class MedicationUpdate(BaseModel):
    anvisa_code: str | None = None
    name : str  | None = None
    description : str | None = None
    
