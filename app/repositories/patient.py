from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from psycopg2 import errors

from fastapi import HTTPException
from app.schemas.patient import PatientIn, PatientOut, PatientUpdate

def create_patient(patient: PatientIn, session: Session):
    existing_patient = (
        session.execute(
            text("""
                SELECT * FROM patient
                WHERE cpf = :cpf
            """),
            {'cpf': patient.cpf},
        ).mappings().first()
    )

    if existing_patient is not None:
        return None
    
    session.execute(
        text("""
             INSERT INTO patient
             (cpf)
            VALUES
            (:cpf)
        """),
        patient.model_dump(),
    )

    session.commit()

    return select_patient_by_cpf(patient.cpf, session)

def select_patient_by_cpf(patient_cpf: str, session: Session):
    result = (
        session.execute(
            text("""
            SELECT 
                p.cpf AS patient_cpf,
                u.id AS user_id,
                u.cpf AS user_cpf,
                u.name,
                u.phone_number,
                u.birthdate,
                u.email
            FROM patient p
            JOIN "user" u ON u.cpf = p.cpf
            WHERE p.cpf = :patient_cpf
        """),
            {'patient_cpf': patient_cpf},
        ).mappings().first()
    )
    
    if result is None:
        return None

    return {
            "cpf": result["patient_cpf"],
            "user": {
                "id": result['user_id'],
                "cpf": result["user_cpf"],
                "name": result["name"],
                "phone_number": result["phone_number"],
                "birthdate": result["birthdate"],
                "email": result["email"]
            }
        }
    

def select_all_patients(session: Session):
    result = session.execute(
        text("""
            SELECT 
                p.cpf AS patient_cpf,
                u.id AS user_id,
                u.cpf AS user_cpf,
                u.name,
                u.phone_number,
                u.birthdate,
                u.email
            FROM patient p
            JOIN "user" u ON u.cpf = p.cpf
        """)
    ).mappings().all()

    return [
        {
            "cpf": row["patient_cpf"],
            "user": {
                "id": row['user_id'],
                "cpf": row["user_cpf"],
                "name": row["name"],
                "phone_number": row["phone_number"],
                "birthdate": row["birthdate"],
                "email": row["email"]
            }
        }
        for row in result
    ]


# def update_patient(patient_update: PatientUpdate, cpf : str, session: Session):
#     patient = (
#         session.execute(
#             text("""
#             SELECT * FROM patient
#             WHERE cpf = :cpf
#         """),
#             {'cpf': cpf},
#         ).mappings().first()
#     )

#     if patient is None:
#         return None
    
#     session.execute(
#         text("""
#         UPDATE patient
#         SET cpf = :cpf
#         WHERE cpf = :cpf
#     """),
#         {**patient_update.model_dump()},
#     )
#     session.commit()

#     return select_patient_by_cpf(patient.cpf, session)

def delete_patient(cpf: str, session: Session):
    result = select_patient_by_cpf(cpf, session)
    
    if result is None:
        return None

    try:

        session.execute(
            text("""
                DELETE FROM patient
                WHERE cpf = :cpf
            """),
            {'cpf': cpf},
        )

        session.commit()
    except IntegrityError as e:
        session.rollback()

        if isinstance(e.orig, errors.ForeignKeyViolation):
            raise HTTPException(409, "Foreign key constraint violated")

        if isinstance(e.orig, errors.UniqueViolation):
            raise HTTPException(409, "Duplicate value")

        if isinstance(e.orig, errors.NotNullViolation):
            raise HTTPException(400, "Required field is missing")

        raise HTTPException(400, "Database constraint error")


    return result