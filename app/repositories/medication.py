from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.medication import MedicationIn, MedicationUpdate


def create_Medication(Medication: MedicationIn, session: Session):

    existing_Medication = (
        session.execute(
            text("""
            SELECT * FROM "medication"
            WHERE anvisa_code = :code
        """),
            {'code': Medication.anvisa_code},
        )
        .mappings()
        .first()
    )

    if existing_Medication is not None:
        return None

    try:
        session.execute(
            text("""
                INSERT INTO "medication"
                (anvisa_code, name, description)
                VALUES
                (:anvisa_code, :name, :description)
            """),
            Medication.model_dump(),
        )

        session.commit()
    except IntegrityError as e:
        session.rollback()
        return None 

    db_Medication = (
        session.execute(
            text("""
            SELECT * FROM "medication"
            WHERE anvisa_code = :code
        """),
            {'code': Medication.anvisa_code},
        )
        .mappings()
        .first()
    )

    return db_Medication


def select_Medication(code: str, session: Session):
    Medication = (
        session.execute(
            text("""
            SELECT * FROM "medication"
            WHERE anvisa_code = :code
        """),
            {'code': code},
        )
        .mappings()
        .first()
    )

    if Medication is None:
        return None

    return dict(Medication)


def select_all_Medications(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "medication"
        """)
        )
        .mappings()
        .fetchall()
    )

    Medications = [dict(row) for row in result]

    return Medications


def update_Medication(Medication_info: MedicationUpdate, code: str, session: Session):

    Medication = (
        session.execute(
            text("""
            SELECT * FROM "medication"
            WHERE anvisa_code = :code
        """),
            {'code': code},
        )
        .mappings()
        .first()
    )

    if Medication is None:
        return None

    session.execute(
        text("""
            UPDATE "medication" SET
                name = :name,
                description = :description
            WHERE anvisa_code = :code
        """),
        {**Medication_info.model_dump(), 'code': code},
    )

    session.commit()

    updated_Medication = (
        session.execute(
            text("""
            SELECT * FROM "medication"
            WHERE anvisa_code = :code
        """),
            {'code': code},
        )
        .mappings()
        .first()
    )

    return updated_Medication


def delete_Medication_db(code: str, session: Session):

    Medication = (
        session.execute(
            text("""
            SELECT * FROM "medication"
            WHERE anvisa_code = :code
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if Medication is None:
        return None

    session.execute(
        text("""
            DELETE FROM "medication"
            WHERE anvisa_code = :code
        """),
        {'code': code},
    )

    session.commit()

    return dict(Medication)
