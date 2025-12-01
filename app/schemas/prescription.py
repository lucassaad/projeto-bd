from pydantic import BaseModel, Field


class PrescriptionBase(BaseModel):
    description: str


class PrescriptionIn(PrescriptionBase):
    appointment_id: int


class PrescriptionOut(PrescriptionBase):
    id: int
    appointment_id: int


class PrescriptionUpdate(PrescriptionBase):
    pass
