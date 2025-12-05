from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.specialty import SpecialtyIn, SpecialtyUpdate


def create_specialty(specialty: SpecialtyIn, session: Session):

    session.execute(
        text("""
            INSERT INTO "specialty"
            (name)
            VALUES
            (:name)
        """),
        specialty.model_dump(),
    )

    session.commit()

    db_specialty = (
        session.execute(
            text("""
            SELECT * FROM "specialty"
            WHERE name = :name
        """),
            {'name': specialty.name},
        )
        .mappings()
        .first()
    )

    return db_specialty


def select_specialty(code: int, session: Session):
    specialty = (
        session.execute(
            text("""
            SELECT * FROM "specialty"
            WHERE code = :code
        """),
            {'code': code},
        )
        .mappings()
        .first()
    )

    if specialty is None:
        return None

    return dict(specialty)


def select_all_specialty(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "specialty"
        """)
        )
        .mappings()
        .fetchall()
    )

    specialty = [dict(row) for row in result]

    return specialty


def update_specialty(
    specialty_info: SpecialtyUpdate, code: int, session: Session
):

    specialty = (
        session.execute(
            text("""
            SELECT * FROM "specialty"
            WHERE  code = :code
        """),
            {'code': code},
        )
        .mappings()
        .first()
    )

    if specialty is None:
        return None

    session.execute(
        text("""
            UPDATE "specialty" SET
                name = :name
            WHERE code = :code
        """),
        {**specialty_info.model_dump(), 'code': code},
    )

    session.commit()

    updated_specialty = (
        session.execute(
            text("""
            SELECT * FROM "specialty"
            WHERE code = :code
        """),
            {'code': code},
        )
        .mappings()
        .first()
    )

    return updated_specialty


def delete_specialty_db(code: int, session: Session):

    specialty = (
        session.execute(
            text("""
            SELECT * FROM "specialty"
            WHERE code = :code
        """),
            {'code': code},
        )
        .mappings()
        .first()
    )

    if specialty is None:
        return None

    session.execute(
        text("""
            DELETE FROM "specialty"
            WHERE code = :code
        """),
        {'code': code},
    )

    session.commit()

    return dict(specialty)
