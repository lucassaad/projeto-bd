from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.nurse import (
    create_nurse,
    delete_nurse_db,
    select_all_nurses,
    select_nurse_by_coren,
    select_nurse_by_cpf,
    update_nurse,
)
from app.schemas.nurse import NurseIn, NurseOut, NurseUpdate

router = APIRouter(prefix='/nurse', tags=['Nurse'])


@router.post('/', response_model=NurseOut, status_code=HTTPStatus.CREATED)
def post_nurse(
    nurse_in: NurseIn, session: Annotated[Session, Depends(get_session)]
):
    nurse = create_nurse(nurse_in, session)
    if nurse is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nurse with given CORen and CPF already exists',
        )
    return nurse


@router.get('/cpf', response_model=NurseOut, status_code=HTTPStatus.OK)
def get_nurse_by_cpf(
    nurse_cpf: str, session: Annotated[Session, Depends(get_session)]
):
    nurse = select_nurse_by_cpf(nurse_cpf, session)
    if nurse is None:
        raise HTTPException(status_code=404, detail='Nurse not found')
    return nurse


@router.get('/coren', response_model=NurseOut, status_code=HTTPStatus.OK)
def get_nurse_by_coren(
    nurse_coren: str, session: Annotated[Session, Depends(get_session)]
):
    nurse = select_nurse_by_coren(nurse_coren, session)
    if nurse is None:
        raise HTTPException(status_code=404, detail='Nurse not found')
    return nurse


@router.get('/all', response_model=list[NurseOut], status_code=HTTPStatus.OK)
def get_all_nurses(session: Annotated[Session, Depends(get_session)]):
    return select_all_nurses(session)


@router.put('/cpf', response_model=NurseOut, status_code=HTTPStatus.OK)
def put_nurse(
    cpf: str,
    nurse_update: NurseUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    nurse = update_nurse(nurse_update, cpf, session)
    if nurse is None:
        raise HTTPException(status_code=404, detail='Nurse not found')
    return nurse


@router.delete('/cpf', response_model=NurseOut, status_code=HTTPStatus.OK)
def delete_nurse(cpf: str, session: Annotated[Session, Depends(get_session)]):
    nurse = delete_nurse_db(cpf, session)
    if nurse is None:
        raise HTTPException(status_code=404, detail='Nurse not found')
    return nurse
