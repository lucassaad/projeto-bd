from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.medication_prescription import Medication_preIn, Medication_preUpdate, Medication_preOut

def create_medication_prescription(medication_prescription: Medication_preIn, session: Session):

    existing_medication_prescription = (
        session.execute(
            text("""
            SELECT * FROM "medication_prescription"
            WHERE 
                medication_code = :medication_code AND
                prescription_id = :prescription_id
        """),
            {
                'medication_code': medication_prescription.medication_code,
                'prescription_id': medication_prescription.prescription_id
            },
        )
        .mappings()
        .first()
    )

    if existing_medication_prescription is not None:
        return None
    try:
        session.execute(
            text("""
                INSERT INTO "medication_prescription"
                (medication_code, prescription_id)
                VALUES
                (:medication_code, :prescription_id)
            """),
            medication_prescription.model_dump(),
        )

        session.commit()
    except IntegrityError as e:
        session.rollback()
        return None

    db_medication_prescription = (
        session.execute(
            text("""
            SELECT * FROM "medication_prescription"
            WHERE 
                medication_code = :medication_code AND
                prescription_id = :prescription_id
        """),
            {
                'medication_code': medication_prescription.medication_code,
                'prescription_id': medication_prescription.prescription_id
            },
        ).mappings().first()
    )

    return db_medication_prescription

def select_medication_prescription(medication_code: str, session: Session):
    medication_prescription = (
        session.execute(
            text("""
            SELECT * FROM "medication_prescription"
            WHERE medication_code = :medication_code
        """),
            {'medication_code': medication_code},
        ).mappings().first()
    )
    if medication_prescription is None:
        return None 
    return medication_prescription

def select_all_medication_prescriptions(session: Session):
    medication_prescriptions = (
        session.execute(
            text("""
            SELECT * FROM "medication_prescription"
        """),
        ).mappings().all()
    )

    return medication_prescriptions

def update_medication_prescription(medication_code: str, medication_prescription_info: Medication_preUpdate, session: Session):

    medication_prescription = (
        session.execute(
            text("""
            SELECT * FROM "medication_prescription"
            WHERE medication_code = :medication_code
        """),
            {'medication_code': medication_code},
        )
        .mappings()
        .first()
    )

    if medication_prescription is None:
        return None

    session.execute(
        text("""
            UPDATE "medication_prescription" SET
                prescription_id = :prescription_id
            WHERE medication_code = :medication_code
        """),
        {**medication_prescription_info.model_dump(), 'medication_code': medication_code},
    )

    session.commit()

    updated_medication_prescription = (
        session.execute(
            text("""
            SELECT * FROM "medication_prescription"
            WHERE medication_code = :medication_code
        """),
            {'medication_code': medication_code},
        )
        .mappings()
        .first()
    )

    return updated_medication_prescription

def delete_medication_prescription_db(medication_code: str, session: Session):

    medication_prescription = (
        session.execute(
            text("""
            SELECT * FROM "medication_prescription"
            WHERE medication_code = :medication_code
        """),
            {'medication_code': medication_code},
        )
        .mappings()
        .first()
    )

    if medication_prescription is None:
        return None

    session.execute(
        text("""
            DELETE FROM "medication_prescription"
            WHERE medication_code = :medication_code
        """),
        {'medication_code': medication_code},
    )

    session.commit()