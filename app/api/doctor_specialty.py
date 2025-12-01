from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.doctor_specialty import (
    create_doctor_specialty,
    select_doctor_by_specialty,
    select_specialty_by_doctor,
    get_all_doctor_specialties,
    update_doctor_specialty,
    delete_doctor_specialty_db,
)
from app.schemas.doctor_specialty import DoctorSpecialtyBase, DoctorSpecialtyIn,DoctorSpecialtyOut

router = APIRouter(prefix='/doctor-specialty', tags=['Doctor_Specialty'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=DoctorSpecialtyOut, status_code=HTTPStatus.CREATED)
def post_doctor_specialty(doc_in: DoctorSpecialtyIn, session: db_session):
    user = create_doctor_specialty(doc_in, session)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Doctor and specialty already exists'
        )
    return user


@router.get('/specialty', response_model=DoctorSpecialtyOut, status_code=HTTPStatus.OK)
def get_doctor_by_specialty(code: int, db_session: db_session):
    user = select_user(code, db_session)

    if user is None:
        raise HTTPException(status_code=404, detail='No doctor found for this specialty')

    return user


@router.get('/doctor', response_model=DoctorSpecialtyOut, status_code=HTTPStatus.OK)
def get_specialty_by_doctor(cpf: str, db_session: db_session):
    user = select_specialty_by_doctor(cpf, db_session)

    if user is None:
        raise HTTPException(status_code=404, detail='No specialty found for this doctor')

    return user

@router.get('/all', response_model=list[DoctorSpecialtyOut], status_code=HTTPStatus.OK)
def get_all_doctors_specialties(db_session: db_session):
    return get_all_doctor_specialties(db_session)


@router.put('/{id}', response_model=DoctorSpecialtyOut, status_code=HTTPStatus.OK)
def put_user(id: int, user_update: DoctorSpecialtyIn, db_session: db_session):
    user = update_doctor_specialty(user_update, id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='Doctor and specialty not found')

    return user


@router.delete('/{id}', response_model=DoctorSpecialtyOut, status_code=HTTPStatus.OK)
def delete_user(id: int, db_session: db_session):
    user = delete_user_db(id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user
