from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.patient import PatientIn, PatientOut, PatientUpdate

def create_patient(patient: PatientIn, session: Session):
    existing_patient = (
        session.execute(
            text("""
            SELECT * FROM patient
            WHERE cpf = :cpf
        """),
        {'cpf': patient.cpf},
        )
        .mappings()
        .first()
    )

    if existing_patient is not None:
        return None
    
    session.execute(
        text("""
             INSERT INTO patient
             (cpf, name, birth_date)
            VALUES
            (:cpf, :name, :birth_date)
    """),
    patient.model_dump(),
    )
    session.commit()

    db_patient = (
        session.execute(
            text("""
            SELECT * FROM patient
            WHERE cpf = :cpf
        """),
            {'cpf': patient.cpf},
        )
        .mappings()
        .first()
    )


    return db_patient

def select_patient_by_cpf(patient_cpf: str, session: Session):
    patient = (
        session.execute(
            text("""
            SELECT * FROM patient
            WHERE cpf = :patient_cpf
        """),
            {'patient_cpf': patient_cpf},
        )
        .mappings()
        .first()
    )

    if patient is None:
        return None

    return patient

def select_all_patients(session: Session):
    patients = (
        session.execute(
            text("""
            SELECT * FROM patient
        """),
        )
        .mappings()
        .all()
    )

    return patients

def update_patient(patient_update: PatientUpdate, id : int, session: Session):
    patient = (
        session.execute(
            text("""
            SELECT * FROM patient
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if patient is None:
        return None
    
    session.execute(
        text("""
        UPDATE patient
        SET cpf = :cpf
        WHERE id = :id
    """),
    {**patient_update.model_dump(), 'id': id},
)
    session.commit()

    updated_patient = (
        session.execute(
            text("""
            SELECT * FROM patient
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_patient

def delete_patient(id: int, session: Session):
    patient = (
        session.execute(
            text("""
            SELECT * FROM patient
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if patient is None:
        return None

    session.execute(
        text("""
            DELETE FROM patient
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return patient