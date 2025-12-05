from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.detailed_appointments import get_detailed_appointments

router = APIRouter(
    prefix='/detailed_appointments', tags=['Detailed Appointments']
)

db_session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=200)
def list_detailed_appointments(session: db_session):
    try:
        result = get_detailed_appointments(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
