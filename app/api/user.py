from http import HTTPStatus
from typing import Annotated

from fastapi.responses import Response
from fastapi import APIRouter, Depends, HTTPException,  UploadFile, File
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.user import (
    create_user,
    delete_user_db,
    select_all_users,
    select_user,
    update_user,
    select_user_photo,
    insert_user_photo
)
from app.schemas.user import UserIn, UserOut, UserUpdate
from app.models.user import User

router = APIRouter(prefix='/user', tags=['User'])

db_session = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=UserOut, status_code=HTTPStatus.OK)
def get_user(cpf: str, db_session: db_session):
    user = select_user(cpf, db_session)


@router.get('/all', response_model=list[UserOut], status_code=HTTPStatus.OK)
def get_all_users(db_session: db_session):
    return select_all_users(db_session)


@router.get("/{id}/photo")
def get_user_photo(id: int, db_session: db_session):
    return select_user_photo(id, db_session)
 

@router.post('/auth', response_model=UserOut, status_code=HTTPStatus.OK)
def autenticate_user(cpf: str, password: str, db_session: db_session):
    user = select_user(cpf, db_session)

    if user is None or user['password'] != password:
        raise HTTPException(status_code=401, detail='Invalid credentials')

    return user


@router.post('/', response_model=UserOut, status_code=HTTPStatus.CREATED)
def post_user(user_in: UserIn, session: db_session):
    user = create_user(user_in, session)
    if user == "email": 
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists'
        )
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='CPF already exists'
        )
    return user


@router.post("/{user_id}/photo")
async def upload_user_photo(
    user_id: int,
    db_session: db_session,
    file: UploadFile = File(...),
):
    return await insert_user_photo(user_id, db_session, file)
    
    
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
