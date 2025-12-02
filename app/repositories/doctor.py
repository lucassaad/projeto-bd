from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.doctor import DoctorIn, DoctorOut, DoctorBase, DoctorUpdate


from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from sqlalchemy.orm import Session
from psycopg2.errors import ForeignKeyViolation


def create_doctor(doctor_in: DoctorIn, session: Session):

    # Verificar duplicado
    existing_doctor = (
        session.execute(
            text("""
                SELECT *
                FROM "doctor"
                WHERE cpf = :cpf
            """),
            {"cpf": doctor_in.cpf}
        ).mappings().first()
    )

    if existing_doctor:
        return {"error": "This doctor does not exist."}

    # Tentar inserir
    try:
        session.execute(
            text("""
                INSERT INTO Doctor (cpf, crm)
                VALUES (:cpf, :crm)
            """),
            doctor_in.model_dump()
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
    return select_doctor_by_cpf(doctor_in.cpf, session)



def select_doctor_by_cpf(cpf: str, session: Session):
    result = (
        session.execute(
            text("""
            SELECT 
                crm as doctor_crm,
                u.id AS user_id,
                u.cpf AS user_cpf,
                u.name,
                u.phone_number,
                u.birthdate,
                u.email
            FROM doctor d 
            JOIN "user" u ON u.cpf = d.cpf
            WHERE d.cpf = :doctor_cpf
        """),
            {'doctor_cpf': cpf},
        ).mappings().first()
    )

    if result is None:
        return None

    return {
            "crm": result["doctor_crm"],
            "user": {
                "id": result['user_id'],
                "cpf": result["user_cpf"],
                "name": result["name"],
                "phone_number": result["phone_number"],
                "birthdate": result["birthdate"],
                "email": result["email"]
            }
        }



def select_all_doctors(session: Session):
    result = (
        session.execute(
            text("""
            SELECT 
                crm as doctor_crm,
                u.id AS user_id,
                u.cpf AS user_cpf,
                u.name,
                u.phone_number,
                u.birthdate,
                u.email
            FROM doctor d 
            JOIN "user" u ON u.cpf = d.cpf
        """),
        ).mappings().all()
    )

    return [
        {
            "crm": row["doctor_crm"],
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


def update_doctor(doctor_info: DoctorUpdate, cpf: str, session: Session):

    result = select_doctor_by_cpf(cpf, session)

    if result is None:
        return None

    session.execute(
        text("""
            UPDATE "doctor" 
            SET
                crm = :crm,
                cpf = :cpf
            WHERE cpf = :cpf
        """),
        {**doctor_info.model_dump(), "cpf": cpf},
    )

    session.commit()

    return select_doctor_by_cpf(cpf, session)


def delete_doctor_db(cpf: str, session: Session):

    result = select_doctor_by_cpf(cpf, session)

    if result is None:
        return None

    session.execute(
        text("""
            DELETE FROM "doctor"
            WHERE cpf = :cpf
        """),
        {'cpf': cpf},
    )

    session.commit()

    return result
