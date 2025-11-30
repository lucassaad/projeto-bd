from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.user import UserIn, UserUpdate


def create_user(user: UserIn, session: Session):

    existing_user = (
        session.execute(
            text("""
            SELECT * FROM "user"
            WHERE cpf = :cpf
        """),
            {'cpf': user.cpf},
        )
        .mappings()
        .first()
    )

    if existing_user is not None:
        return None

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

    db_user = (
        session.execute(
            text("""
            SELECT * FROM "user"
            WHERE cpf = :cpf
        """),
            {'cpf': user.cpf},
        )
        .mappings()
        .first()
    )

    return db_user


def select_user(cpf: str, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "user"
            WHERE cpf = :cpf
        """),
            {'cpf': cpf},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    return dict(user)


def select_all_users(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "user"
        """)
        )
        .mappings()
        .fetchall()
    )

    users = [dict(row) for row in result]

    return users


def update_user(user_info: UserUpdate, id: int, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "user"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    session.execute(
        text("""
            UPDATE "user" SET
                cpf = :cpf,
                name = :name,
                phone_number = :phone_number,
                birthdate = :birthdate,
                email = :email,
                password = :password
            WHERE id = :id
        """),
        {**user_info.model_dump(), 'id': id},
    )

    session.commit()

    updated_user = (
        session.execute(
            text("""
            SELECT * FROM "user"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_user


def delete_user_db(id: int, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "user"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    session.execute(
        text("""
            DELETE FROM "user"
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(user)
