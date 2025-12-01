from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.nurse import NurseIn, NurseOut, NurseUpdate

def create_nurse(nurse: NurseIn, session: Session):
    existing_nurse = (
        session.execute(
            text("""
            SELECT * FROM nurse
            WHERE coren = :coren AND cpf = :cpf
        """),
        {'coren': nurse.coren, 'cpf': nurse.cpf},
        )
        .mapping()
        .first()
    )

    if existing_nurse is not None:
        return None
    
    session.execute(
        text("""
             INSERT INTO nurse
             (nurse_cpf, coren)
            VALUES
            (:nurse_cpf, :coren)
    """),
    nurse.model_dump(),
    )
    session.commit()

    db_nurse = (
        session.execute(
            text("""text
            SELECT * FROM nurse
            WHERE coren = :coren AND cpf = :cpf
        """),
            {'coren': nurse.coren, 'cpf': nurse.cpf},
        )
        .mappings()
        .first()
    )


    return db_nurse

def select_nurse_by_cpf(nurse_cpf: str, session: Session):
    nurse = (
        session.execute(
            text("""
            SELECT * FROM nurse
            WHERE nurse_cpf = :nurse_cpf
        """),
            {'nurse_cpf': nurse_cpf},
        )
        .mappings()
        .first()
    )

    if nurse is None:
        return None

    return nurse

def select_nurse_by_coren(coren: str, session: Session):
    nurse = (
        session.execute(
            session.execute(
                text("""
                SELECT * FROM nurse
                WHERE coren = :coren
            """),
                {'coren': coren},
            )
        )
        .mappings()
        .first()
    )

    if nurse is None:
        return None
    
    return nurse

def select_all_nurses(session: Session):
    nurses = (
        session.execute(
            text("""
            SELECT * FROM nurse
        """)
        )
        .mappings()
        .fetchall()
    )

    return nurses

def update_nurse(nurse_update: NurseUpdate, id: int, session: Session):
    nurse = (
        session.execute(
            text("""
            SELECT * FROM nurse
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if nurse is None:
        return None
    
    session.execute(
        text("""
            UPDATE nurse
            SET coren = :coren,
            cpf = :cpf
            WHERE id = :id
        """),
        {**nurse_update.model_dump(), 'id': nurse['id']},
    )

    session.commit()

    updated_nurse = (
        session.execute(
            text("""
            SELECT * FROM nurse
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_nurse

def delete_nurse(id: int, session: Session):
    nurse = (
        session.execute(
            text("""
            SELECT * FROM nurse
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if nurse is None:
        return None

    session.execute(
        text("""
            DELETE FROM nurse
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(nurse)