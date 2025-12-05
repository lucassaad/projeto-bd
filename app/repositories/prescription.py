from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.prescription import PrescriptionIn, PrescriptionUpdate


def create_prescription(prescription: PrescriptionIn, session: Session):

    existing_prescription = (
        session.execute(
            text("""
            SELECT * FROM "prescription"
            WHERE 
                appointment_id = :appointment_id
        """),
            {'appointment_id': prescription.appointment_id},
        )
        .mappings()
        .first()
    )

    if existing_prescription is not None:
        return None

    session.execute(
        text("""
            INSERT INTO "prescription"
            (appointment_id, description)
            VALUES
            (:appointment_id, :description)
        """),
        prescription.model_dump(),
    )

    session.commit()

    db_prescription = (
        session.execute(
            text("""
            SELECT * FROM "prescription"
            WHERE 
                appointment_id = :appointment_id
        """),
            {'appointment_id': prescription.appointment_id},
        )
        .mappings()
        .first()
    )

    return db_prescription


def select_prescription(id: str, session: Session):
    prescription = (
        session.execute(
            text("""
            SELECT * FROM "prescription"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if prescription is None:
        return None

    return dict(prescription)


def select_all_prescriptions(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "prescription"
        """)
        )
        .mappings()
        .fetchall()
    )

    prescription = [dict(row) for row in result]

    return prescription


def update_prescription(
    prescription_info: PrescriptionUpdate, id: int, session: Session
):

    prescription = (
        session.execute(
            text("""
            SELECT * FROM "prescription"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if prescription is None:
        return None

    session.execute(
        text("""
            UPDATE "prescription" SET
                description = :description
            WHERE id = :id
        """),
        {
            **prescription_info.model_dump(),
            'id': id,
            'appointment_id': prescription.appointment_id,
        },
    )

    session.commit()

    updated_prescription = (
        session.execute(
            text("""
            SELECT * FROM "prescription"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_prescription


def delete_prescription_db(id: int, session: Session):

    prescription = (
        session.execute(
            text("""
            SELECT * FROM "prescription"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if prescription is None:
        return None

    session.execute(
        text("""
            DELETE FROM "prescription"
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(prescription)
