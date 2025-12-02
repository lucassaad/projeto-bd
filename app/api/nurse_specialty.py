from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.nurse_specialty import (
    create_nurse_specialty,
    delete_nurse_specialty_db,
    select_all_nurse_specialties,
    select_specialty_by_nurse,
    select_specialty_by_name,
    select_nurse_specialty_by_id,
    update_nurse_specialty,
)
from app.schemas.nurse_specialty import (
    Nurse_specialtyIn,
    Nurse_specialtyOut,
    Nurse_specialtyUpdate,
)

router = APIRouter(prefix="/nurse_specialty", tags=["Nurse_specialty"])

db_session = Annotated[Session, Depends(get_session)]


@router.post("/", response_model=Nurse_specialtyOut, status_code=HTTPStatus.CREATED)
def post_nurse_specialty(nurse_specialty_in: Nurse_specialtyIn, session: db_session):
    nurse_specialty = create_nurse_specialty(nurse_specialty_in, session)
    if nurse_specialty is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Nurse_specialty already exists"
        )
    return nurse_specialty


@router.get("/nurse", response_model=Nurse_specialtyOut)
def get_nurse_specialty(nurse_cpf: str, session: db_session):
    nurse_specialty = select_specialty_by_nurse(nurse_cpf, session)
    if nurse_specialty is None:
        raise HTTPException(status_code=404, detail="Nurse_specialty not found")
    return nurse_specialty


@router.get("/name", response_model=Nurse_specialtyOut)
def get_specialty_by_name(specialty: str, session: db_session):
    nurse_specialty = select_specialty_by_name(specialty, session)
    if nurse_specialty is None:
        raise HTTPException(status_code=404, detail="Nurse_specialty not found")
    return nurse_specialty


@router.get("/id", response_model=Nurse_specialtyOut)
def get_nurse_specialty_by_id(id: int, session: db_session):
    nurse_specialty = select_nurse_specialty_by_id(id, session)
    if nurse_specialty is None:
        raise HTTPException(status_code=404, detail="Nurse_specialty not found")
    return nurse_specialty


@router.get("/all", response_model=list[Nurse_specialtyOut])
def get_all_nurse_specialties(db_session: db_session):
    return select_all_nurse_specialties(db_session)


@router.put("/{id}", response_model=Nurse_specialtyOut)
def put_nurse_specialty(id: int, nurse_specialty_update: Nurse_specialtyUpdate, session: db_session):
    nurse_specialty = update_nurse_specialty(nurse_specialty_update, id, session)
    if nurse_specialty is None:
        raise HTTPException(status_code=404, detail="Nurse_specialty not found")
    return nurse_specialty


@router.delete("/{id}", response_model=Nurse_specialtyOut)
def delete_nurse_specialty(id: int, session: db_session):
    nurse_specialty = delete_nurse_specialty_db(id, db_session)
    if nurse_specialty is None:
        raise HTTPException(status_code=404, detail="Nurse_specialty not found")
    return nurse_specialty
