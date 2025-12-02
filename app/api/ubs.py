from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.ubs import UbsIn, UbsOut, UbsUpdate
from app.repositories.ubs import (
    create_ubs,
    select_all_ubs,
    delete_ubs_db,
    select_ubs,
    update_ubs
)


router = APIRouter(prefix='/ubs', tags=['Ubs'])
db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=UbsOut, status_code=HTTPStatus.CREATED)
def post_ubs(ubs_in: UbsIn, session: db_session):
    ubs = create_ubs(ubs_in, session)
    if ubs is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='UBS already exists'
        )
    return ubs


@router.get('/', response_model=UbsOut, status_code=HTTPStatus.OK)
def get_ubs(cnes: str, db_session: db_session):
    ubs = select_ubs(cnes, db_session)

    if ubs is None:
        raise HTTPException(status_code=404, detail='UBS not found')

    return ubs


@router.get('/all', response_model=list[UbsOut], status_code=HTTPStatus.OK)
def get_all_ubs(db_session: db_session):
    return select_all_ubs(db_session)


@router.put('/cnes', response_model=UbsOut, status_code=HTTPStatus.OK)
def put_ubs(ubs_update: UbsUpdate, cnes: str, db_session: db_session):
    ubs = update_ubs(ubs_update, cnes, db_session)
    if ubs is None:
        raise HTTPException(status_code=404, detail='UBS not found')

    return ubs


@router.delete('/cnes', response_model=UbsOut, status_code=HTTPStatus.OK)
def delete_ubs(cnes: str, db_session: db_session):
    ubs = delete_ubs_db(cnes, db_session)
    if ubs is None:
        raise HTTPException(status_code=404, detail='UBS not found')

    return ubs
