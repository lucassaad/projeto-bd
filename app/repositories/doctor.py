from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.doctor import DoctorIn, DoctorOut, DoctorBase, DoctorUpdate


from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from sqlalchemy.orm import Session
from psycopg2.errors import ForeignKeyViolation


def create_Doctor(Doctor_in: DoctorIn, session: Session):

    # Verificar duplicado
    existing = (
        session.execute(
            text("""
                SELECT *
                FROM "doctor"
                WHERE cpf = :cpf OR crm = :crm
            """),
            {
                "crm": Doctor_in.crm,
                "cpf": Doctor_in.cpf
            }
        )
        .mappings()
        .first()
    )

    if existing:
        return {"error": "This doctor does not exist."}

    # Tentar inserir
    try:
        session.execute(
            text("""
                INSERT INTO Doctor (cpf, crm)
                VALUES (:cpf, :crm)
            """),
            Doctor_in.model_dump()
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
                FROM Doctor
                WHERE cpf = :cpf AND ubs_cnes = :cnes
            """),
            {
                "cpf": Doctor_in.doctor_cpf,
                "cnes": Doctor_in.cnes_ubs
            }
        )
        .mappings()
        .first()
    )

    return db_row



def select_doctor_by_cpf(cpf: str, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "Doctor"
            WHERE cpf = :cpf
        """),
            {'cpf': cpf},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    return dict(user)



def get_all_Doctor(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "Doctor"
        """)
        )
        .mappings()
        .fetchall()
    )

    users = [dict(row) for row in result]

    return users


def update_Doctor(Doctor_info: DoctorIn, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "Doctor"
            WHERE cpf = :cpf
        """),
            {'cpf': Doctor_info.cpf},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    session.execute(
        text("""
            UPDATE "Doctor" SET
                crm = :crm
            WHERE cpf = :cpf
        """),
        {**Doctor_info.model_dump()},
    )

    session.commit()

    updated_user = (
        session.execute(
            text("""
            SELECT * FROM "Doctor"
            WHERE cpf = :cpf
        """),
            {'cpf': Doctor_info.cpf},
        )
        .mappings()
        .first()
    )

    return updated_user


def delete_Doctor_db(cpf: str, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "Doctor"
            WHERE cpf = :cpf
        """),
            {'cpf': cpf},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    session.execute(
        text("""
            DELETE FROM "Doctor"
            WHERE cpf = :cpf
        """),
        {'cpf': cpf},
    )

    session.commit()

    return dict(user)
