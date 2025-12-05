from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.specialty import (
    create_specialty,
    delete_specialty_db,
    select_all_specialty,
    select_specialty,
    update_specialty,
)
from app.schemas.specialty import SpecialtyIn, SpecialtyOut, SpecialtyUpdate

router = APIRouter(prefix='/specialty', tags=['specialty'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=SpecialtyOut, status_code=HTTPStatus.CREATED)
def post_specialty(specialty_in: SpecialtyIn, session: db_session):
    specialty = create_specialty(specialty_in, session)

    return specialty


@router.get('/', response_model=SpecialtyOut, status_code=HTTPStatus.OK)
def get_specialty(code: int, db_session: db_session):
    specialty = select_specialty(code, db_session)

    if specialty is None:
        raise HTTPException(status_code=404, detail='Specialty not found')

    return specialty


@router.get(
    '/all', response_model=list[SpecialtyOut], status_code=HTTPStatus.OK
)
def get_all_specialty(db_session: db_session):
    return select_all_specialty(db_session)


@router.put('/{id}', response_model=SpecialtyOut, status_code=HTTPStatus.OK)
def put_specialty(
    id: int, specialty_update: SpecialtyUpdate, db_session: db_session
):
    specialty = update_specialty(specialty_update, id, db_session)
    if specialty is None:
        raise HTTPException(status_code=404, detail='Specialty not found')

    return specialty


@router.delete('/{id}', response_model=SpecialtyOut, status_code=HTTPStatus.OK)
def delete_specialty(code: int, db_session: db_session):
    specialty = delete_specialty_db(code, db_session)
    if specialty is None:
        raise HTTPException(status_code=404, detail='Specialty not found')

    return specialty
