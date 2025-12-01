from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.nurse_specialty import Nurse_specialtyIn, Nurse_specialtyOut, Nurse_specialtyUpdate

def create_nurse_specialty(nurse_specialty: Nurse_specialtyIn, session: Session):

    existing_nurse_specialty = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
            WHERE nurse_cpf = :nurse_cpf ANDspecialty = specialty
        """),
            {'nurse_cpf': nurse_specialty.nurse_cpf, 'specialty': nurse_specialty},
        )
        .mappings()
        .first()
    )

    if existing_nurse_specialty is not None:
        return None
    
    session.execute(
        text("""
            INSERT INTO nurse_specialty
            (nurse_cpf,specialty)
            VALUES
            (:nurse_cpf, specialty)
        """),
        nurse_specialty.model_dump(),
    )

    session.commit()

    db_nurse_specialty = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
            WHERE nurse_cpf = :nurse_cpf ANDspecialty = specialty
        """),
            {'nurse_cpf': nurse_specialty.nurse_cpf, 'specialty': nurse_specialty},
        )
        .mapping()
        .first()
    )

    return db_nurse_specialty

def select_specialty_by_nurse(nurse_cpf: str, session: Session):
    nurse_specialty = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
            WHERE nurse_cpf = :nurse_cpf
        """),
            {'nurse_cpf': nurse_cpf},
        )
        .mappings()
        .first()
    )

    if nurse_specialty is None:
        return None
    
    return dict(nurse_specialty)

def select_specialty_by_name(specialty: str, session: Session):
    nurse_specialty = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
            WHEREspecialty = specialty
        """),
            {'specialty':specialty},
        )
        .mappings()
        .first()
    )

    if nurse_specialty is None:
        return None
    
    return dict(nurse_specialty)

def select_nurse_specialty_by_id(id: int, session: Session):
    nurse_specialty = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if nurse_specialty is None:
        return None
    
    return dict(nurse_specialty)

def select_all_nurse_specialties(session: Session):
    nurse_specialities = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
        """),
        )
        .mappings()
        .all()
    )

    return nurse_specialities

def update_nurse_specialty(nurse_specialty_info: Nurse_specialtyUpdate, id: int, session: Session):
    nurse_specialty = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if nurse_specialty is None:
        return None

    session.execute(
        text("""
            UPDATE nurse_specialty SET
            nurse_cpf = :nurse_cpf,
            specialty = :specialty
            WHERE id = :id
    """),
    {**nurse_specialty_info.model_dump(), 'id': id},
    )

    session.commit()

    uptaded_nurse_specialty = (
        session.execute(
            text("""
            SELECT * FROM nurse_specialty
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return uptaded_nurse_specialty

def delete_nurse_specialty_db(id: int, session: Session):
    nurse_specialty = (
        session.execute(
            text("""text
            SELECT * FROM nurse_specialty
            WHERE id = :id
        """),
            {'id': id}, 
        )
        .mappings()
        .first()
    )

    if nurse_specialty is None:
        return None
    
    session.execute(
        text("""
        DELETE FROM nurse_specialty
        WHERE id = :id
    """),
        {id: id},
    )

    session.commit()

    return dict(nurse_specialty)