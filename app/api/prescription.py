from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.prescription import (
    create_prescription,
    delete_prescription_db,
    select_all_prescriptions,
    select_prescription,
    update_prescription,
)
from app.schemas.prescription import (
    PrescriptionIn,
    PrescriptionOut,
    PrescriptionUpdate,
)

router = APIRouter(prefix='/prescription', tags=['Prescription'])

db_session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', response_model=PrescriptionOut, status_code=HTTPStatus.CREATED
)
def post_prescription(prescription_in: PrescriptionIn, session: db_session):
    prescription = create_prescription(prescription_in, session)
    if prescription is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='CPF already exists'
        )
    return prescription


@router.get('/', response_model=PrescriptionOut, status_code=HTTPStatus.OK)
def get_prescription(cpf: str, db_session: db_session):
    prescription = select_prescription(cpf, db_session)

    if prescription is None:
        raise HTTPException(status_code=404, detail='prescription not found')

    return prescription


@router.get(
    '/all', response_model=list[PrescriptionOut], status_code=HTTPStatus.OK
)
def get_all_prescriptions(db_session: db_session):
    return select_all_prescriptions(db_session)


@router.put('/{id}', response_model=PrescriptionOut, status_code=HTTPStatus.OK)
def put_prescription(
    id: int, prescription_update: PrescriptionUpdate, db_session: db_session
):
    prescription = update_prescription(prescription_update, id, db_session)
    if prescription is None:
        raise HTTPException(status_code=404, detail='prescription not found')

    return prescription


@router.delete(
    '/{id}', response_model=PrescriptionOut, status_code=HTTPStatus.OK
)
def delete_prescription(id: int, db_session: db_session):
    prescription = delete_prescription_db(id, db_session)
    if prescription is None:
        raise HTTPException(status_code=404, detail='prescription not found')

    return prescription
