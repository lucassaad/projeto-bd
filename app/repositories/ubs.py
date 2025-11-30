from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.ubs import UbsIn, UbsUpdate


def create_ubs(ubs: UbsIn, session: Session):

    existing_ubs = (
        session.execute(
            text("""
            SELECT * FROM "ubs"
            WHERE  cnes= :cnes
        """),
            {'cnes': ubs.cnes},
        )
        .mappings()
        .first()
    )

    if existing_ubs is not None:
        return None

    session.execute(
        text("""
            INSERT INTO "ubs"
            (cnes, name, addres)
            VALUES
            (:cnes, :name, :addres)
        """),
        ubs.model_dump(),
    )

    session.commit()

    db_ubs = (
        session.execute(
            text("""
            SELECT * FROM "ubs"
            WHERE cnes = :cnes
        """),
            {'cnes': ubs.cnes},
        )
        .mappings()
        .first()
    )

    return db_ubs


def select_ubs(cnes: str, session: Session):
    ubs = (
        session.execute(
            text("""
            SELECT * FROM "ubs"
            WHERE cnes = :cnes
        """),
            {'cnes': cnes},
        )
        .mappings()
        .first()
    )

    if ubs is None:
        return None

    return dict(ubs)


def select_all_ubs(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "ubs"
        """)
        )
        .mappings()
        .fetchall()
    )

    ubs = [dict(row) for row in result]

    return ubs


def update_ubs(ubs_info: UbsUpdate, cnes: str, session: Session):

    ubs = (
        session.execute(
            text("""
            SELECT * FROM "ubs"
            WHERE cnes = :cnes
        """),
            {'cnes': cnes},
        )
        .mappings()
        .first()
    )

    if ubs is None:
        return None

    session.execute(
        text("""
            UPDATE "ubs" SET
                cnes = :cnes,
                name = :name,
                addres = :addres
            WHERE cnes = :cnes
        """),
        {**ubs_info.model_dump(), 'cnes': cnes},
    )

    session.commit()

    updated_ubs = (
        session.execute(
            text("""
            SELECT * FROM "ubs"
            WHERE cnes = :cnes
        """),
            {'cnes': cnes},
        )
        .mappings()
        .first()
    )

    return updated_ubs


def delete_ubs_db(cnes: str, session: Session):

    ubs = (
        session.execute(
            text("""
            SELECT * FROM "ubs"
            WHERE cnes = :cnes
        """),
            {'cnes': cnes},
        )
        .mappings()
        .first()
    )

    if ubs is None:
        return None

    session.execute(
        text("""
            DELETE FROM "ubs"
            WHERE cnes = :cnes
        """),
        {'cnes': cnes},
    )

    session.commit()

    return dict(ubs)
