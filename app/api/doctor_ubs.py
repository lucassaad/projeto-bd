from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.doctor_ubs import (
    create_doctor_ubs,
    select_doctor_by_ubs,
    select_ubs_by_doctor,
    get_all_doctor_ubs,
    update_doctor_ubs,
    delete_doctor_ubs_db,
)
from app.schemas.doctor_ubs import Doctor_ubsBase, Doctor_ubsIn,Doctor_ubsOut

router = APIRouter(prefix='/doctor-ubs', tags=['doctor_ubs'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=Doctor_ubsOut, status_code=HTTPStatus.CREATED)
def post_doctor_ubs(doc_in: Doctor_ubsIn, session: db_session):
    user = create_doctor_ubs(doc_in, session)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Doctor already exists in UBS'
        )
    return user


@router.get('/ubs', response_model=Doctor_ubsOut, status_code=HTTPStatus.OK)
def get_doctor_by_ubs(code: str, db_session: db_session):
    user =select_doctor_by_ubs(code, db_session)

    if user is None:
        raise HTTPException(status_code=404, detail='No doctor found in this UBS')

    return user


@router.get('/doctor', response_model=Doctor_ubsOut, status_code=HTTPStatus.OK)
def get_ubs_by_doctor(cpf: str, db_session: db_session):
    user = select_ubs_by_doctor(cpf, db_session)

    if user is None:
        raise HTTPException(status_code=404, detail='No ubs found for this doctor')

    return user

@router.get('/all', response_model=list[Doctor_ubsOut], status_code=HTTPStatus.OK)
def get_all_doctor_ubs(db_session: db_session):
    return get_all_doctor_ubs(db_session)


@router.put('/{id}', response_model=Doctor_ubsOut, status_code=HTTPStatus.OK)
def put_user(id: int, user_update: Doctor_ubsIn, db_session: db_session):
    user = update_doctor_ubs(user_update, id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='Doctor and ubs not found')

    return user


@router.delete('/{id}', response_model=Doctor_ubsOut, status_code=HTTPStatus.OK)
def delete_user(id: int, db_session: db_session):
    user = delete_doctor_ubs_db(id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user
