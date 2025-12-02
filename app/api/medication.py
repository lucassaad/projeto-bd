from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.medication import (
    create_Medication,
    select_Medication,
    select_all_Medications,
    update_Medication,
    delete_Medication_db,
)
from app.schemas.medication import MedicationBase, MedicationIn,MedicationOut

router = APIRouter(prefix='/medication', tags=['Medication'])

db_session = Annotated[Session, Depends(get_session)]

@router.post('/', response_model=MedicationOut, status_code=HTTPStatus.CREATED)
def post_Medication(med_in: MedicationIn, session: db_session):
    med = create_Medication(med_in, session)
    if med is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Medication prescription already exists'
        )
    return med


@router.get('/pre', response_model=MedicationOut, status_code=HTTPStatus.OK)
def get_Medication(medication_code: str, db_session: db_session):
    med = select_Medication(medication_code, db_session)

    if med is None:
        raise HTTPException(status_code=404, detail='Medication prescription not found')

    return med

@router.get('/all', response_model=list[MedicationOut], status_code=HTTPStatus.OK)
def get_all_Medications(db_session: db_session):
    return select_all_Medications(db_session) 



@router.put('/{id}', response_model=MedicationOut, status_code=HTTPStatus.OK)
def put_Medication(id: int, med_update: MedicationIn, db_session: db_session):
    med = update_Medication(med_update, id, db_session)
    if med is None:
        raise HTTPException(status_code=404, detail='Medication prescription not found')

    return med

@router.delete('/{id}', response_model=MedicationOut, status_code=HTTPStatus.OK)
def delete_Medication(id: int, db_session: db_session):
    med = delete_Medication_db(id, db_session)
    if med is None:
        raise HTTPException(status_code=404, detail='Medication prescription not found')
    return med


