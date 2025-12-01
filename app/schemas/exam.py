from datetime import date

from pydantic import BaseModel, Field


class ExamBase(BaseModel):
    exam_date: date
    exam_type: str

class ExamIn(ExamBase):
    appointment_id: int


class ExamOut(ExamBase):
    id: int
    appointment_id: int


class ExamUpdate(ExamBase):
    pass
