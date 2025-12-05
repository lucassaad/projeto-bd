from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.vaccine import VaccineIn, VaccineUpdate


def create_vaccine(vaccine: VaccineIn, session: Session):

    existing_vaccine = (
        session.execute(
            text("""
            SELECT * FROM "vaccine"
            WHERE 
                patient_cpf = :patient_cpf
            AND
                nurse_cpf = :nurse_cpf
            AND 
                name = :name
        """),
            {
                'patient_cpf': vaccine.patient_cpf,
                'nurse_cpf': vaccine.nurse_cpf,
                'name': vaccine.name,
            },
        )
        .mappings()
        .first()
    )

    if existing_vaccine is not None:
        return None

    session.execute(
        text("""
            INSERT INTO "vaccine"
            (patient_cpf, nurse_cpf, name, description, manufacturer)
            VALUES
            (:patient_cpf, :nurse_cpf, :name, :description, :manufacturer)
        """),
        vaccine.model_dump(),
    )

    session.commit()

    db_vaccine = (
        session.execute(
            text("""
            SELECT * FROM "vaccine"
            WHERE 
                patient_cpf = :patient_cpf
            AND
                nurse_cpf = :nurse_cpf
            AND 
                name = :name
        """),
            {
                'patient_cpf': vaccine.patient_cpf,
                'nurse_cpf': vaccine.nurse_cpf,
                'name': vaccine.name,
            },
        )
        .mappings()
        .first()
    )

    return db_vaccine


def select_vaccine(id: int, session: Session):
    vaccine = (
        session.execute(
            text("""
            SELECT * FROM "vaccine"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if vaccine is None:
        return None

    return dict(vaccine)


def select_all_vaccines(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "vaccine"
        """)
        )
        .mappings()
        .fetchall()
    )

    vaccines = [dict(row) for row in result]

    return vaccines


def update_vaccine(vaccine_info: VaccineUpdate, id: int, session: Session):

    vaccine = (
        session.execute(
            text("""
            SELECT * FROM "vaccine"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if vaccine is None:
        return None

    session.execute(
        text("""
            UPDATE "vaccine" SET
                name = :name,
                description = :description,
                manufacturer = :manufacturer
            WHERE id = :id
        """),
        {**vaccine_info.model_dump(), 'id': id},
    )

    session.commit()

    updated_vaccine = (
        session.execute(
            text("""
            SELECT * FROM "vaccine"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_vaccine


def delete_vaccine_db(id: int, session: Session):

    vaccine = (
        session.execute(
            text("""
            SELECT * FROM "vaccine"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if vaccine is None:
        return None

    session.execute(
        text("""
            DELETE FROM "vaccine"
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(vaccine)
