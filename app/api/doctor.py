from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.doctor import (
    create_Doctor,
    select_doctor_by_cpf,
    get_all_Doctor,
    update_Doctor,
    delete_Doctor_db,
)
from app.schemas.doctor import DoctorBase, DoctorIn,DoctorOut

router = APIRouter(prefix='/doctor', tags=['Doctor'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=DoctorOut, status_code=HTTPStatus.CREATED)
def post_Doctor(doc_in: DoctorIn, session: db_session):
    user = create_Doctor(doc_in, session)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Doctor already exists in UBS'
        )
    return user


@router.get('/cpf', response_model=DoctorOut, status_code=HTTPStatus.OK)
def get_doctor_by_cpf(code: str, db_session: db_session):
    user =select_doctor_by_cpf(code, db_session)

    if user is None:
        raise HTTPException(status_code=404, detail='No doctor found in this UBS')

    return user



@router.get('/all', response_model=list[DoctorOut], status_code=HTTPStatus.OK)
def get_all_Doctor(db_session: db_session):
    return get_all_Doctor(db_session)


@router.put('/{id}', response_model=DoctorOut, status_code=HTTPStatus.OK)
def put_user(user_update: DoctorIn, db_session: db_session):
    user = update_Doctor(user_update, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='Doctor and ubs not found')

    return user


@router.delete('/{id}', response_model=DoctorOut, status_code=HTTPStatus.OK)
def delete_user(cpf: str, db_session: db_session):
    user = delete_Doctor_db(cpf, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user
