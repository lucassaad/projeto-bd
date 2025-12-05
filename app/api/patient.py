from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.patient import (
    create_patient,
    # update_patient,
    delete_patient,
    select_all_patients,
    select_patient_by_cpf,
)
from app.schemas.patient import PatientIn, PatientOut

router = APIRouter(prefix='/patient', tags=['Patient'])


@router.post('/', response_model=PatientOut, status_code=HTTPStatus.CREATED)
def post_patient(
    patient_in: PatientIn, session: Annotated[Session, Depends(get_session)]
):
    patient = create_patient(patient_in, session)
    if patient is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Patient with given CPF already exists',
        )
    return patient


@router.get('/cpf', response_model=PatientOut, status_code=HTTPStatus.OK)
def get_patient_by_cpf(
    patient_cpf: str, session: Annotated[Session, Depends(get_session)]
):
    patient = select_patient_by_cpf(patient_cpf, session)
    if patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient


@router.get('/all', response_model=list[PatientOut], status_code=HTTPStatus.OK)
def get_all_patients(session: Annotated[Session, Depends(get_session)]):
    return select_all_patients(session)


# @router.put('/{cpf}', response_model=PatientOut, status_code=HTTPStatus.OK)
# def put_patient(cpf: str, patient_update: PatientUpdate, session: Annotated[Session, Depends(get_session)]):
#     patient = update_patient(patient_update, cpf, session)
#     if patient is None:
#         raise HTTPException(status_code=404, detail='Patient not found')
#     return patient


@router.delete('/cpf}', response_model=PatientOut, status_code=HTTPStatus.OK)
def delete_patient_route(
    cpf: str, session: Annotated[Session, Depends(get_session)]
):
    patient = delete_patient(cpf, session)
    if patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient
