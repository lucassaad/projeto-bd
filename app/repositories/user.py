from fastapi import File, HTTPException, Response, UploadFile
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.user import User
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

    try:
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

    except Exception:
        session.rollback()
        return 'email'
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


def select_user_photo(id: int, session: Session):
    user = session.scalar(select(User).where(User.id == id))

    if not user or not user.image:
        raise HTTPException(status_code=404, detail='Image not found')

    return Response(content=user.image, media_type='image/png')


async def insert_user_photo(
    user_id: int,
    session: Session,
    file: UploadFile = File(...),
):
    if file.content_type is None or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='Invalid file type')

    # Limite de 2MB, por exemplo
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(status_code=413, detail='File too large')

    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user.image = content
    session.commit()

    return {'message': 'Photo uploaded successfully'}
