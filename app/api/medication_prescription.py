from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.medication_prescription import (
    create_medication_prescription,
    delete_medication_prescription_db,
    select_all_medication_prescriptions,
    select_medication_prescription,
    update_medication_prescription,
)
from app.schemas.medication_prescription import (
    Medication_preIn,
    Medication_preOut,
)

router = APIRouter(prefix='/medication-pre', tags=['Medication_Prescription'])

db_session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', response_model=Medication_preOut, status_code=HTTPStatus.CREATED
)
def post_medication_prescription(
    med_in: Medication_preIn, session: db_session
):
    med = create_medication_prescription(med_in, session)
    if med is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Medication prescription already exists',
        )
    return med


@router.get(
    '/pre', response_model=Medication_preOut, status_code=HTTPStatus.OK
)
def get_medication_prescription(medication_code: str, db_session: db_session):
    med = select_medication_prescription(medication_code, db_session)

    if med is None:
        raise HTTPException(
            status_code=404, detail='Medication prescription not found'
        )

    return med


@router.get(
    '/all', response_model=list[Medication_preOut], status_code=HTTPStatus.OK
)
def get_all_medication_prescriptions(db_session: db_session):
    return select_all_medication_prescriptions(db_session)


@router.put(
    '/{id}', response_model=Medication_preOut, status_code=HTTPStatus.OK
)
def put_medication_prescription(
    id: int, med_update: Medication_preIn, db_session: db_session
):
    med = update_medication_prescription(med_update, id, db_session)
    if med is None:
        raise HTTPException(
            status_code=404, detail='Medication prescription not found'
        )

    return med


@router.delete(
    '/{id}', response_model=Medication_preOut, status_code=HTTPStatus.OK
)
def delete_medication_prescription(id: int, db_session: db_session):
    med = delete_medication_prescription_db(id, db_session)
    if med is None:
        raise HTTPException(
            status_code=404, detail='Medication prescription not found'
        )
    return med
