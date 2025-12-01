from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.exam import (
    create_exam,
    delete_exam_db,
    select_all_exams,
    select_exam,
    update_exam
)
from app.schemas.exam import ExamIn, ExamOut, ExamUpdate

router = APIRouter(prefix='/exam', tags=['Exam'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=ExamOut, status_code=HTTPStatus.CREATED)
def post_exam(exam_in: ExamIn, session: db_session):
    exam = create_exam(exam_in, session)
    if exam is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='CPF already exists'
        )
    return exam


@router.get('/', response_model=ExamOut, status_code=HTTPStatus.OK)
def get_exam(cpf: str, db_session: db_session):
    exam = select_exam(cpf, db_session)

    if exam is None:
        raise HTTPException(status_code=404, detail='exam not found')

    return exam


@router.get('/all', response_model=list[ExamOut], status_code=HTTPStatus.OK)
def get_all_exams(db_session: db_session):
    return select_all_exams(db_session)


@router.put('/{id}', response_model=ExamOut, status_code=HTTPStatus.OK)
def put_exam(id: int, exam_update: ExamUpdate, db_session: db_session):
    exam = update_exam(exam_update, id, db_session)
    if exam is None:
        raise HTTPException(status_code=404, detail='exam not found')

    return exam


@router.delete('/{id}', response_model=ExamOut, status_code=HTTPStatus.OK)
def delete_exam(id: int, db_session: db_session):
    exam = delete_exam_db(id, db_session)
    if exam is None:
        raise HTTPException(status_code=404, detail='exam not found')

    return exam
