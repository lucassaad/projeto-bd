from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.doctor import (
    create_doctor,
    delete_doctor_db,
    select_all_doctors,
    select_doctor_by_cpf,
    select_view,
    update_doctor,
)
from app.schemas.doctor import DoctorIn, DoctorOut, DoctorUpdate
from app.schemas.view import ViewOut

router = APIRouter(prefix='/doctor', tags=['Doctor'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=DoctorOut, status_code=HTTPStatus.CREATED)
def post_doctor(doctor_in: DoctorIn, session: db_session):
    user = create_doctor(doctor_in, session)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Doctor already exists in UBS',
        )
    return user


@router.get('/cpf', response_model=DoctorOut, status_code=HTTPStatus.OK)
def get_doctor_by_cpf(cpf: str, db_session: db_session):
    user = select_doctor_by_cpf(cpf, db_session)

    if user is None:
        raise HTTPException(
            status_code=404, detail='No doctor found in this UBS'
        )

    return user


@router.get('/view', response_model=list[ViewOut], status_code=HTTPStatus.OK)
def get_view(db_session: db_session):
    user = select_view(db_session)

    if user is None:
        raise HTTPException(
            status_code=404, detail='No doctor found in this UBS'
        )

    return user


@router.get('/all', response_model=list[DoctorOut], status_code=HTTPStatus.OK)
def get_all_doctors(db_session: db_session):
    return select_all_doctors(db_session)


@router.put('/cpf', response_model=DoctorOut, status_code=HTTPStatus.OK)
def put_doctor(cpf: str, doctor_update: DoctorUpdate, db_session: db_session):
    user = update_doctor(doctor_update, cpf, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='Doctor and ubs not found')

    return user


@router.delete('/cpf', response_model=DoctorOut, status_code=HTTPStatus.OK)
def delete_user(cpf: str, db_session: db_session):
    user = delete_doctor_db(cpf, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='Doctor not found')

    return user
