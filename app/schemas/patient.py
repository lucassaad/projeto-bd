from datetime import date

from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    birth_date: date


class PatientIn(PatientBase):
    pass


class PatientOut(PatientBase):
    pass

class PatientUpdate(PatientBase):
    name: str | None = None
    birth_date: date | None = None
