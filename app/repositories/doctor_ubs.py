from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.doctor_ubs import Doctor_ubsIn, Doctor_ubsOut, Doctor_ubsBase, Doctor_ubsUpdate


from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from sqlalchemy.orm import Session
from psycopg2.errors import ForeignKeyViolation


def create_doctor_ubs(doctor_ubs_in: Doctor_ubsIn, session: Session):

    # Verificar duplicado
    existing = (
        session.execute(
            text("""
                SELECT *
                FROM "doctor_ubs"
                WHERE doctor_cpf = :cpf AND ubs_cnes = :cnes
            """),
            {
                "cpf": doctor_ubs_in.doctor_cpf,
                "cnes": doctor_ubs_in.cnes_ubs
            }
        )
        .mappings()
        .first()
    )

    if existing:
        return {"error": "There is already an association between this doctor and UBS."}

    # Tentar inserir
    try:
        session.execute(
            text("""
                INSERT INTO doctor_ubs (doctor_cpf, ubs_cnes)
                VALUES (:doctor_cpf, :cnes_ubs)
            """),
            doctor_ubs_in.model_dump()
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
                FROM doctor_ubs
                WHERE doctor_cpf = :cpf AND ubs_cnes = :cnes
            """),
            {
                "cpf": doctor_ubs_in.doctor_cpf,
                "cnes": doctor_ubs_in.cnes_ubs
            }
        )
        .mappings()
        .first()
    )

    return db_row



def select_ubs_by_doctor(cpf: str, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_ubs"
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


def select_doctor_by_ubs(cnes: str, session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "doctor_ubs"
            WHERE ubs_cnes = :cnes
        """), 
            {'cnes': cnes},
        )
        .mappings()
        .fetchall()
    )

    users = [dict(row) for row in result]

    return users


def get_all_doctor_ubs(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "doctor_ubs"
        """)
        )
        .mappings()
        .fetchall()
    )

    users = [dict(row) for row in result]

    return users


def update_doctor_ubs(doctor_ubs_info: Doctor_ubsIn, id: int, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_ubs"
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
            UPDATE "doctor_ubs" SET
                doctor_cpf = :doctor_cpf,
                ubs_cnes = :cnes_ubs
            WHERE id = :id
        """),
        {**doctor_ubs_info.model_dump(), 'id': id},
    )

    session.commit()

    updated_user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_ubs"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_user


def delete_doctor_ubs_db(id: int, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "doctor_ubs"
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
            DELETE FROM "doctor_ubs"
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(user)
