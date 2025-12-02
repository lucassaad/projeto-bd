from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.nurse_ubs import (
    create_nurse_ubs,
    delete_nurse_ubs_db,
    select_all_nurse_ubs,
    select_nurse_ubs_by_nurse,
    select_nurse_ubs_by_id,
    select_nurse_ubs_by_ubs,
    update_nurse_ubs,
)
from app.schemas.nurse_ubs import Nurse_ubsIn, Nurse_ubsOut, Nurse_ubsUpdate

router = APIRouter(prefix='/user', tags=['Nurse_ubs'])

db_session = Annotated[Session, Depends(get_session)]

@router.post('/', response_model=Nurse_ubsOut, status_code=HTTPStatus.CREATED)
def post_nurse_ubs(nurse_ubs_in: Nurse_ubsIn, session: db_session):
    nurse_ubs = create_nurse_ubs(nurse_ubs_in, session)
    if nurse_ubs is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Nurse_ubs already exists'
        )
    return nurse_ubs

@router.get('/nurse', response_model=Nurse_ubsOut, status_code=HTTPStatus.OK)
def get_nurse_ubs(nurse_cpf: str, ubs_cnes: str, db_session: db_session):
    nurse_ubs = select_nurse_ubs_by_nurse(nurse_cpf, ubs_cnes, db_session)
    if nurse_ubs is None:
        raise HTTPException(status_code=404, detail='Nurse_ubs not found')
    return nurse_ubs

@router.get('/ubs', response_model=Nurse_ubsOut, status_code=HTTPStatus.OK)
def get_nurse_ubs_by_ubs(ubs_cnes: str, db_session: db_session):
    nurse_ubs = select_nurse_ubs_by_ubs(ubs_cnes, db_session)
    if nurse_ubs is None:
        raise HTTPException(status_code=404, detail='Nurse_ubs not found')
    return nurse_ubs

@router.get('/{id}', response_model=Nurse_ubsOut, status_code=HTTPStatus.OK)
def get_nurse_ubs_by_id(id: int, db_session: db_session):
    nurse_ubs = select_nurse_ubs_by_id(id, db_session)
    if nurse_ubs is None:
        raise HTTPException(status_code=404, detail='Nurse_ubs not found')
    return nurse_ubs

@router.get('/all', response_model=list[Nurse_ubsOut], status_code=HTTPStatus.OK)
def get_all_nurse_ubs(db_session: db_session):
    return select_all_nurse_ubs(db_session)

@router.put('/{id}', response_model=Nurse_ubsOut, status_code=HTTPStatus.OK)
def put_nurse_ubs(id: int, nurse_ubs_update: Nurse_ubsUpdate, db_session: db_session):
    nurse_ubs = update_nurse_ubs(nurse_ubs_update, id, db_session)
    if nurse_ubs is None:
        raise HTTPException(status_code=404, detail='Nurse_ubs not found')
    return nurse_ubs

@router.delete('/{id}', response_model=Nurse_ubsOut, status_code=HTTPStatus.OK)
def delete_nurse_ubs(id: int, db_session: db_session):
    nurse_ubs = delete_nurse_ubs_db(id, db_session)
    if nurse_ubs is None:
        raise HTTPException(status_code=404, detail='Nurse_ubs not found')
    return nurse_ubs
