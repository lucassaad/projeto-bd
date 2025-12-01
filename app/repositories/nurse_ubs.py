from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.user import Nurse_ubsIn, Nurse_ubsOut, Nurse_ubsUpdate

def create_nurse_ubs(nurse_ubs: Nurse_ubsIn, session: Session):

    existing_nurse_ubs = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
            WHERE nurse_cpf = :nurse_cpf AND ubs_cnes = :ubs_cnes
        """),
            {'nurse_cpf': nurse_ubs.nurse_cpf, 'ubs_cnes': nurse_ubs.ubs_cnes},
        )
        .mappings()
        .first()
    )

    if existing_nurse_ubs is not None:
        return None

    session.execute(
        text("""
            INSERT INTO nurse_ubs
            (nurse_cpf, ubs_cnes)
            VALUES
            (:nurse_cpf, :ubs_cnes)
        """),
        nurse_ubs.model_dump(),
    )

    session.commit()

    db_nurse_ubs = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
            WHERE nurse_cpf = :nurse_cpf AND ubs_cnes = :ubs_cnes
        """),
            {'nurse_cpf': nurse_ubs.nurse_cpf, 'ubs_cnes': nurse_ubs.ubs_cnes},
        )
        .mappings()
        .first()
    )

    return db_nurse_ubs

def select_nurse_ubs(nurse_cpf: str, ubs_cnes: str, session: Session):
    nurse_ubs = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
            WHERE nurse_cpf = :nurse_cpf AND ubs_cnes = :ubs_cnes
        """),
            {'nurse_cpf': nurse_cpf, 'ubs_cnes': ubs_cnes},
        )
        .mappings()
        .first()
    )

    return nurse_ubs

    if nurse_ubs is None:
        return None
    
    return dict(nurse_ubs)

def select_nurse_ubs(id: int, session: Session):
    nurse_ubs = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
            WHERE id = :id
        """)
        )
        .mappings()
        .all()
    )

    if user is None:
        return None
    
    return dict(nurse_ubs)

def select_all_nurse_ubs(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
        """)
        )
        .mappings()
        .fetchall()
    )

    nurse_ubs = [dict(row) for row in result]

    return nurse_ubs

def update_nurse_ubs(nurse_ubs_info: Nurse_ubsUpdate, id: int, session: Session):

    nurse_ubs = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if nurse_ubs is None:
        return None

    updated_nurse_ubs = nurse_ubs_info.model_dump()

    session.execute(
        text("""
            UPDATE nurse_ubs
            SET nurse_cpf = :nurse_cpf,
            ubs_cnes = :ubs_cnes
            WHERE id = :id
        """),
        {**updated_nurse_ubs, 'id': id},
    )

    session.commit()

    updated_nurse_ubs = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_nurse_ubs

def delete_nurse_ubs_db(id: int, session: Session):
    nurse_ubs = (
        session.execute(
            text("""
            SELECT * FROM nurse_ubs
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if nurse_ubs is None:
        return None

    session.execute(
        text("""
            DELETE FROM nurse_ubs
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(nurse_ubs)


