from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.doctor_specialty import (
    DoctorSpecialtyIn,
)


def create_doctor_specialty(
    doctor_specialty_in: DoctorSpecialtyIn, session: Session
):

    # Verificar duplicado
    existing = (
        session.execute(
            text("""
                SELECT *
                FROM doctor_specialty
                WHERE doctor_cpf = :cpf AND specialty_code = :specialty_code
            """),
            {
                'cpf': doctor_specialty_in.doctor_cpf,
                'specialty_code': doctor_specialty_in.specialty_code,
            },
        )
        .mappings()
        .first()
    )

    if existing:
        return {'error': 'This doctor already has this specialty.'}

    # Tentar inserir
    try:
        session.execute(
            text("""
                INSERT INTO doctor_specialty (doctor_cpf, specialty_code)
                VALUES (:doctor_cpf, :specialty_code)
            """),
            doctor_specialty_in.model_dump(),
        )
        session.commit()

    except IntegrityError as e:
        session.rollback()

        # CASO O MÉDICO NÃO EXISTA NA TABELA doctor
        if isinstance(e.orig, ForeignKeyViolation):
            return None

        # outros erros de integridade
        return None

    # Buscar registro final inserido
    db_row = (
        session.execute(
            text("""
                SELECT *
                FROM doctor_specialty
                WHERE doctor_cpf = :cpf AND specialty_code = :specialty_code
            """),
            {
                'cpf': doctor_specialty_in.doctor_cpf,
                'specialty_code': doctor_specialty_in.specialty_code,
            },
        )
        .mappings()
        .first()
    )

    return db_row


def select_specialty_by_doctor(cpf: str, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_specialty"
            WHERE doctor_cpf = :cpf
        """),
            {'cpf': cpf},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    return dict(user)


def select_doctor_by_specialty(code: int, session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "doctor_specialty"
            WHERE specialty_code = :code
        """),
            {'code': code},
        )
        .mappings()
        .fetchall()
    )

    users = [dict(row) for row in result]

    return users


def get_all_doctor_specialties(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "doctor_specialty"
        """)
        )
        .mappings()
        .fetchall()
    )

    users = [dict(row) for row in result]

    return users


def update_doctor_specialty(
    doctor_specialty_info: DoctorSpecialtyIn, id: int, session: Session
):

    user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_specialty"
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
            UPDATE "doctor_specialty" SET
                doctor_cpf = :doctor_cpf,
                specialty_code = :specialty_code
            WHERE id = :id
        """),
        {**doctor_specialty_info.model_dump(), 'id': id},
    )

    session.commit()

    updated_user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_specialty"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_user


def delete_doctor_specialty_db(id: int, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_specialty"
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
            DELETE FROM "doctor_specialty"
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(user)
