from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.user import (
    create_user,
    delete_user_db,
    select_all_users,
    select_user,
    update_user,
)
from app.schemas.user import UserIn, UserOut, UserUpdate

router = APIRouter(prefix='/user', tags=['User'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=UserOut, status_code=HTTPStatus.CREATED)
def post_user(user_in: UserIn, session: db_session):
    user = create_user(user_in, session)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='CPF already exists'
        )
    return user


@router.get('/', response_model=UserOut, status_code=HTTPStatus.OK)
def get_user(cpf: str, db_session: db_session):
    user = select_user(cpf, db_session)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@router.get('/all', response_model=list[UserOut], status_code=HTTPStatus.OK)
def get_all_users(db_session: db_session):
    return select_all_users(db_session)


@router.put('/{id}', response_model=UserOut, status_code=HTTPStatus.OK)
def put_user(id: int, user_update: UserUpdate, db_session: db_session):
    user = update_user(user_update, id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@router.delete('/{id}', response_model=UserOut, status_code=HTTPStatus.OK)
def delete_user(id: int, db_session: db_session):
    user = delete_user_db(id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user
