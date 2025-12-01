from pydantic import BaseModel


class DoctorBase(BaseModel):
    name: str
    crm: str


class Doctor(DoctorBase):
    pass

class DoctorOut(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    name: str | None = None
    crm: str | None = None