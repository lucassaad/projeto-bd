from pydantic import BaseModel


class Medication_preBase(BaseModel):
    medication_code: str
    prescription_id: int


class Medication_preIn(Medication_preBase):
    pass


class Medication_preOut(Medication_preBase):
    id: int | None = None
    pass


class Medication_preUpdate(BaseModel):
    pass
