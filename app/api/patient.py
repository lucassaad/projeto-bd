from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.patient import (
    create_patient,
    select_patient_by_cpf,
    select_all_patients,
    update_patient,
    delete_patient
)

from app.schemas.patient import PatientIn, PatientOut, PatientUpdate

router = APIRouter(prefix='/patient', tags=['Patient'])

@router.post('/', response_model=PatientOut, status_code=HTTPStatus.CREATED)
def post_patient(   patient_in: PatientIn, session: Annotated[Session, Depends(get_session)]):
    patient = create_patient(patient_in, session)
    if patient is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Patient with given CPF already exists')
    return patient

@router.get('/cpf/', response_model=PatientOut, status_code=HTTPStatus.OK)