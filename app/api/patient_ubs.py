from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.patient_ubs import (
    create_patient_ubs,
    delete_patient_ubs,
    select_all_patient_ubs,
    select_patient_ubs_by_cnes,
    select_patient_ubs_by_cpf,
    update_patient_ubs,
)
from app.schemas.patient_ubs import (
    Patient_ubsIn,
    Patient_ubsOut,
    Patient_ubsUpdate,
)

router = APIRouter(prefix='/patient_ubs', tags=['Patient_UBS'])

db_session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', response_model=Patient_ubsOut, status_code=HTTPStatus.CREATED
)
def post_patient_ubs(patient_ubs_in: Patient_ubsIn, session: db_session):
    patient_ubs = create_patient_ubs(patient_ubs_in, session)
    if patient_ubs is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Patient UBS association already exists',
        )
    return patient_ubs


@router.get('/cpf', response_model=Patient_ubsOut, status_code=HTTPStatus.OK)
def get_patient_ubs_by_cpf(patient_cpf: str, session: db_session):
    patient_ubs = select_patient_ubs_by_cpf(patient_cpf, session)
    if patient_ubs is None:
        raise HTTPException(
            status_code=404, detail='Patient UBS association not found'
        )
    return patient_ubs


@router.get(
    '/cnes', response_model=list[Patient_ubsOut], status_code=HTTPStatus.OK
)
def get_patient_ubs_by_cnes(ubs_cnes: str, session: db_session):
    patient_ubs = select_patient_ubs_by_cnes(ubs_cnes, session)
    if patient_ubs is None:
        raise HTTPException(
            status_code=404,
            detail='No Patient UBS associations found for this CNES',
        )
    return patient_ubs


@router.get(
    '/all', response_model=list[Patient_ubsOut], status_code=HTTPStatus.OK
)
def get_all_patient_ubs(session: db_session):
    return select_all_patient_ubs(session)


@router.put('/{id}', response_model=Patient_ubsOut, status_code=HTTPStatus.OK)
def put_patient_ubs(
    id: int, patient_ubs_update: Patient_ubsUpdate, session: db_session
):
    patient_ubs = update_patient_ubs(patient_ubs_update, id, session)
    if patient_ubs is None:
        raise HTTPException(
            status_code=404, detail='Patient UBS association not found'
        )
    return patient_ubs


@router.delete(
    '{id}', response_model=Patient_ubsOut, status_code=HTTPStatus.OK
)
def delete_patient_ubs(id: int, session: db_session):
    patient_ubs = delete_patient_ubs(id, session)
    if patient_ubs is None:
        raise HTTPException(
            status_code=404, detail='Patient UBS association not found'
        )
    return patient_ubs
