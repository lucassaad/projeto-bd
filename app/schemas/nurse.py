from pydantic import BaseModel


class NurseBase(BaseModel):
    name: str
    coren: str


class Doctor(NurseBase):
    pass

class DoctorOut(NurseBase):
    pass

class DoctorUpdate(NurseBase):
    name: str | None = None
    coren: str | None = None