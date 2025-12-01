from datetime import datetime

from pydantic import BaseModel   


class MedicationBase(BaseModel):
    anvisa_code: str
    name : str
    description : str


class AppointmentIn(MedicationBase):
    pass


class AppointmentOut(MedicationBase):
    pass


class AppointmentUpdate(MedicationBase):
    anvisa_code: str | None = None
    name : str  | None = None
    description : str | None = None
    
