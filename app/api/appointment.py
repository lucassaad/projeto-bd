from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.appointment import create_appointment
from app.schemas.appointment import AppointmentIn, AppointmentOut

router = APIRouter(prefix='/appointment', tags=['Appointment'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=AppointmentOut, status_code=HTTPStatus.CREATED)
def post_appointment(appointment_in: AppointmentIn, session: db_session):
    return create_appointment(appointment_in, session)
