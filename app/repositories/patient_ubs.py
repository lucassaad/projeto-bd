from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.patient_ubs import Patient_ubsIn, Patient_ubsOut, Patient_ubsUpdate

def create_patient_ubs(patient_ubs: Patient_ubsIn, session: Session):
    existing_patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
            WHERE patient_cpf = :patient_cpf AND ubs_cnes = :ubs_cnes)
        """),
            {'patient_cpf': patient_ubs.patient_cpf, 'ubs_cnes': patient_ubs.ubs_cnes},
        )
        .mapping()
        .first()
    )

    if existing_patient_ubs is not None:
        return None
    
    session.execute(
        text("""
             INSERT INTO patient_ubs
             (patient_cpf, ubs_cnes)
             VALUES
            (:patient_cpf, :ubs_cnes)
    """),
    patient_ubs.model_dump(),
    )
    session.commit()

    db_patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
            WHERE patient_cpf = :patient_cpf AND ubs_cnes = :ubs_cnes
        """),
            {'patient_cpf': patient_ubs.patient_cpf, 'ubs_cnes': patient_ubs.ubs_cnes},
        )
        .mappings()
        .first()
    )

    return db_patient_ubs

def select_patient_ubs_by_cpf(patient_cpf: str, session: Session):
    patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
            WHERE patient_cpf = :patient_cpf
        """),
            {'patient_cpf': patient_cpf},
        )
        .mappings()
        .first()
    )

    if patient_ubs is None:
        return None

    return patient_ubs

def select_patient_ubs_by_cnes(ubs_cnes: str, session: Session):
    patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
            WHERE ubs_cnes = :ubs_cnes
        """),
            {'ubs_cnes': ubs_cnes},
        )
        .mappings()
        .first()
    )

    if patient_ubs is None:
        return None

    return patient_ubs

def select_all_patient_ubs(session: Session):
    patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
        """),
        )
        .mappings()
        .fetchall()
    )

    patients_ubs = [dict(row) for row in patient_ubs]

    return patients_ubs

def update_patient_ubs(patient_ubs_info: Patient_ubsUpdate, id: int, session: Session):

    patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if patient_ubs is None:
        return None

    session.execute(
        text("""
            UPDATE patient_ubs
            SET patient_cpf = :patient_cpf,
            ubs_cnes = :ubs_cnes
            WHERE id = :id
        """),
        { **patient_ubs_info.model_dump(), 'id': id},
    )

    session.commit()

    updated_patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_patient_ubs

def delete_patient_ubs(id: int, session: Session):
    patient_ubs = (
        session.execute(
            text("""
            SELECT * FROM patient_ubs
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if patient_ubs is None:
        return None

    session.execute(
        text("""
            DELETE FROM patient_ubs
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return dict(patient_ubs)