from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.user import UserIn


def create_user(user: UserIn, session: Session):

    session.execute(
        text("""
            INSERT INTO "user"
            (cpf, name, phone_number, birthdate, email, password)
            VALUES
            (:cpf, :name, :phone_number, :birthdate, :email, :password)
        """),
        user.model_dump(),
    )

    session.commit()

    return user
