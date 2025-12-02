from datetime import date

from pydantic import BaseModel, EmailStr, Field


class MedicationBase(BaseModel):
    anvisa_code: str
    name: str
    description: str | None = None

class MedicationIn(MedicationBase):
    pass

class MedicationOut(MedicationBase):
    pass


class MedicationUpdate(MedicationBase):
    password: str
