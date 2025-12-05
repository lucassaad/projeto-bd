from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.appointment import (
    create_appointment,
    delete_appointment_db,
    select_all_appointments,
    select_appointment_cpf_doctor,
    select_appointment_cpf_patient,
    select_appointment_datetime,
    select_appointment_id,
    select_appointment_ubs_cnes,
    update_appointment,
)
from app.schemas.appointment import AppointmentIn, AppointmentOut

router = APIRouter(prefix='/appointments', tags=['Appointment'])

db_session = Annotated[Session, Depends(get_session)]


@router.get(
    '/search', response_model=List[AppointmentOut], status_code=HTTPStatus.OK
)
def search_appointments(
    # type_search corresponde ao 'tipo_busca' no front-end
    type_search: Annotated[str, Query(alias='tipo_busca')],
    # value corresponde ao 'valor' no front-end
    value: Annotated[str, Query(alias='valor')],
    session: db_session,
):
    search_map = {
        'patient_cpf': select_appointment_cpf_patient,
        'doctor_cpf': select_appointment_cpf_doctor,
        'ubs_cnes': select_appointment_ubs_cnes,
        'datetime': select_appointment_datetime,
    }

    if type_search not in search_map:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Invalid search type: {type_search}.',
        )

    try:
        repository_function = search_map[type_search]

        appointments = repository_function(value, session)

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Database error during search: {e}',
        )

    if not appointments:
        return []

    return appointments


@router.post(
    '/', response_model=AppointmentOut, status_code=HTTPStatus.CREATED
)
def post_appointment(appointment_in: AppointmentIn, session: db_session):
    return create_appointment(appointment_in, session)


@router.get(
    '/patient', response_model=list[AppointmentOut], status_code=HTTPStatus.OK
)
def get_appointment_patient(cpf: str, db_session: db_session):
    appointment = select_appointment_cpf_patient(cpf, db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')
    return appointment


@router.get(
    '/doctor', response_model=list[AppointmentOut], status_code=HTTPStatus.OK
)
def get_appointment_doctor(cpf: str, db_session: db_session):
    appointment = select_appointment_cpf_doctor(cpf, db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')
    return appointment


@router.get(
    '/ubs', response_model=list[AppointmentOut], status_code=HTTPStatus.OK
)
def get_appointment_ubs(cnes: str, db_session: db_session):
    appointment = select_appointment_ubs_cnes(cnes, db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')
    return appointment


@router.get(
    '/datetime', response_model=list[AppointmentOut], status_code=HTTPStatus.OK
)
def get_appointment_datetime(date: str, db_session: db_session):
    appointment = select_appointment_datetime(date, db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')
    return appointment


@router.get(
    '/id/{id}', response_model=AppointmentOut, status_code=HTTPStatus.OK
)
def get_appointment_id(id: int, db_session: db_session):
    appointment = select_appointment_id(id, db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')
    return appointment


@router.get(
    '/all', response_model=list[AppointmentOut], status_code=HTTPStatus.OK
)
def get_all_appointments(db_session: db_session):
    appointment = select_all_appointments(db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointments not found')
    return select_all_appointments(db_session)


@router.put('/{id}', response_model=AppointmentOut, status_code=HTTPStatus.OK)
def put_appointment(
    id: int, appointment_update: AppointmentIn, db_session: db_session
):
    appointment = update_appointment(appointment_update, id, db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')

    return appointment


@router.delete(
    '/{id}', response_model=AppointmentOut, status_code=HTTPStatus.OK
)
def delete_appointment(id: int, db_session: db_session):
    appointment = delete_appointment_db(id, db_session)
    if appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')

    return appointment
