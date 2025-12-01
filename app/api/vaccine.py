from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.vaccine import (
    create_vaccine,
    delete_vaccine_db,
    select_all_vaccines,
    select_vaccine,
    update_vaccine
)
from app.schemas.vaccine import VaccineIn, VaccineOut, VaccineUpdate

router = APIRouter(prefix='/vaccine', tags=['Vaccine'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=VaccineOut, status_code=HTTPStatus.CREATED)
def post_vaccine(vaccine_in: VaccineIn, session: db_session):
    vaccine = create_vaccine(vaccine_in, session)
    if vaccine is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Vaccine already exists'
        )
    return vaccine


@router.get('/', response_model=VaccineOut, status_code=HTTPStatus.OK)
def get_vaccine(id: int, db_session: db_session):
    vaccine = select_vaccine(id, db_session)

    if vaccine is None:
        raise HTTPException(status_code=404, detail='Vaccine not found')

    return vaccine


@router.get('/all', response_model=list[VaccineOut], status_code=HTTPStatus.OK)
def get_all_vaccines(db_session: db_session):
    return select_all_vaccines(db_session)


@router.put('/{id}', response_model=VaccineOut, status_code=HTTPStatus.OK)
def put_vaccine(id: int, vaccine_update: VaccineUpdate, db_session: db_session):
    vaccine = update_vaccine(vaccine_update, id, db_session)
    if vaccine is None:
        raise HTTPException(status_code=404, detail='Vaccine not found')

    return vaccine


@router.delete('/{id}', response_model=VaccineOut, status_code=HTTPStatus.OK)
def delete_vaccine(id: int, db_session: db_session):
    vaccine = delete_vaccine_db(id, db_session)
    if vaccine is None:
        raise HTTPException(status_code=404, detail='Vaccine not found')

    return vaccine
