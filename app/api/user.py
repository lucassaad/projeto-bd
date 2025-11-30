from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.user import create_user
from app.schemas.user import UserIn, UserOut

router = APIRouter(prefix='/user', tags=['User'])

db_session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=UserOut, status_code=HTTPStatus.CREATED)
def post_user(user_in: UserIn, session: db_session):
    return create_user(user_in, session)
