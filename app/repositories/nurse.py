from fastapi import HTTPException
from psycopg2 import errors
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.nurse import NurseIn, NurseUpdate


def create_nurse(nurse: NurseIn, session: Session):
    existing_nurse = (
        session.execute(
            text("""
                SELECT * FROM nurse
                WHERE cpf = :cpf
            """),
            {'cpf': nurse.cpf},
        )
        .mappings()
        .first()
    )

    if existing_nurse is not None:
        return None

    session.execute(
        text("""
             INSERT INTO nurse
             (cpf, coren)
            VALUES
            (:cpf, :coren)
    """),
        nurse.model_dump(),
    )
    session.commit()

    return select_nurse_by_cpf(nurse.cpf, session)


def select_nurse_by_cpf(nurse_cpf: str, session: Session):
    result = (
        session.execute(
            text("""
            SELECT 
                n.coren as nurse_coren,
                u.id AS user_id,
                u.cpf AS user_cpf,
                u.name,
                u.phone_number,
                u.birthdate,
                u.email
            FROM nurse n 
            JOIN "user" u ON u.cpf = n.cpf
            WHERE n.cpf = :nurse_cpf
        """),
            {'nurse_cpf': nurse_cpf},
        )
        .mappings()
        .first()
    )

    if result is None:
        return None

    return {
        'coren': result['nurse_coren'],
        'user': {
            'id': result['user_id'],
            'cpf': result['user_cpf'],
            'name': result['name'],
            'phone_number': result['phone_number'],
            'birthdate': result['birthdate'],
            'email': result['email'],
        },
    }


def select_nurse_by_coren(coren: str, session: Session):
    result = (
        session.execute(
            text("""
            SELECT 
                n.coren as nurse_coren,
                u.id AS user_id,
                u.cpf AS user_cpf,
                u.name,
                u.phone_number,
                u.birthdate,
                u.email
            FROM nurse n 
            JOIN "user" u ON u.cpf = n.cpf
            WHERE n.coren = :nurse_coren
        """),
            {'nurse_coren': coren},
        )
        .mappings()
        .first()
    )

    if result is None:
        return None

    return {
        'coren': result['nurse_coren'],
        'user': {
            'id': result['user_id'],
            'cpf': result['user_cpf'],
            'name': result['name'],
            'phone_number': result['phone_number'],
            'birthdate': result['birthdate'],
            'email': result['email'],
        },
    }


def select_all_nurses(session: Session):
    result = (
        session.execute(
            text("""
            SELECT 
                n.coren as nurse_coren,
                u.id AS user_id,
                u.cpf AS user_cpf,
                u.name,
                u.phone_number,
                u.birthdate,
                u.email
            FROM nurse n 
            JOIN "user" u ON u.cpf = n.cpf
        """)
        )
        .mappings()
        .all()
    )

    return [
        {
            'coren': row['nurse_coren'],
            'user': {
                'id': row['user_id'],
                'cpf': row['user_cpf'],
                'name': row['name'],
                'phone_number': row['phone_number'],
                'birthdate': row['birthdate'],
                'email': row['email'],
            },
        }
        for row in result
    ]


def update_nurse(nurse_update: NurseUpdate, cpf: str, session: Session):
    result = select_nurse_by_cpf(cpf, session)

    if result is None:
        return None

    try:
        session.execute(
            text("""
                UPDATE nurse
                SET 
                    coren = :coren,
                    cpf = :cpf
                WHERE cpf = :cpf
            """),
            {**nurse_update.model_dump(), 'cpf': cpf},
        )

        session.commit()

    except IntegrityError as e:
        session.rollback()

        if isinstance(e.orig, errors.ForeignKeyViolation):
            raise HTTPException(409, 'Foreign key constraint violated')

        if isinstance(e.orig, errors.UniqueViolation):
            raise HTTPException(409, 'Duplicate value')

        if isinstance(e.orig, errors.NotNullViolation):
            raise HTTPException(400, 'Required field is missing')

        raise HTTPException(400, 'Database constraint error')

    return select_nurse_by_cpf(cpf, session)


def delete_nurse_db(cpf: str, session: Session):
    result = select_nurse_by_cpf(cpf, session)

    if result is None:
        return None

    session.execute(
        text("""
            DELETE FROM nurse
            WHERE cpf = :cpf
        """),
        {'cpf': cpf},
    )

    session.commit()

    return result
