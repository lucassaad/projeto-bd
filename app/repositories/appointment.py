from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from fastapi import HTTPException
from app.schemas.appointment import AppointmentIn


def create_appointment(appointment_in: AppointmentIn, session: Session):

    p_datetime = appointment_in.date.replace(tzinfo=None)  # REMOVE timezone

    # Montando os parâmetros esperados pela procedure
    params = {
        "doctor_cpf": appointment_in.doctor_cpf,
        "patient_cpf": appointment_in.patient_cpf,
        "ubs_cnes": appointment_in.ubs_cnes,
        "p_datetime": p_datetime,   # use o nome do campo que está no schema
    }

    try:
        # Executa a procedure
        session.execute(
            text("""
                CALL create_appointment(
                    :doctor_cpf,
                    :patient_cpf,
                    :ubs_cnes,
                    :p_datetime
                );
            """),
            params
        )

        # Confirma a transação
        session.commit()
    except DBAPIError as e:
        # pega a mensagem da procedure
        error_msg = str(e.orig)

        # transforma para FastAPI retornar como erro 400
        raise HTTPException(status_code=400, detail=error_msg)

    return {
    "doctor_cpf": appointment_in.doctor_cpf,
    "patient_cpf": appointment_in.patient_cpf,
    "ubs_cnes": appointment_in.ubs_cnes,
    "date": appointment_in.date,

}



def select_appointment_cpf_patient(cpf: str, session: Session):
    rows = (
        session.execute(
            text("""
                SELECT * FROM "appointment"
                WHERE patient_cpf = :cpf
            """),
            {"cpf": cpf}
        )
        .mappings()
        .all()
    )
    if rows is None:
        return None

    appointments = []
    for row in rows:
        appointments.append({
            "doctor_cpf": row["doctor_cpf"],
            "patient_cpf": row["patient_cpf"],
            "ubs_cnes": row["ubs_cnes"],
            "date": row["appointment_datetime"],  # renomeando
            "id": row["id"],
            "message": "Appointment found."
        })

    # Converte os campos para o schema correto
    return appointments

def select_appointment_cpf_doctor(cpf: str, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
            WHERE doctor_cpf = :cpf
        """),
            {'cpf': cpf},
        )
        .mappings()
        .all()
    )

    if user is None:
        return None

    appointments = []
    for row in user:
        appointments.append({
            "doctor_cpf": row["doctor_cpf"],
            "patient_cpf": row["patient_cpf"],
            "ubs_cnes": row["ubs_cnes"],
            "date": row["appointment_datetime"],
            "id": row["id"],
            "message": "Appointment found."
        })

    # Converte os campos para o schema correto
    return appointments

def select_appointment_ubs_cnes(cnes: str, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
            WHERE ubs_cnes = :cnes
        """),
            {'cnes': cnes},
        )
        .mappings()
        .all()
    )

    if user is None:
        return None

    appointments = []
    for row in user:
        appointments.append({
            "doctor_cpf": row["doctor_cpf"],
            "patient_cpf": row["patient_cpf"],
            "ubs_cnes": row["ubs_cnes"],
            "date": row["appointment_datetime"],  # renomeando
            "id": row["id"],
            "message": "Appointment found."
        })

    # Converte os campos para o schema correto
    return appointments

def select_appointment_datetime(appointment_datetime: str, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
            WHERE appointment_datetime = :appointment_datetime
        """),
            {'appointment_datetime': appointment_datetime},
        )
        .mappings()
        .all()
    )

    if user is None:
        return None

    appointments = []
    for row in user:
        appointments.append({
            "doctor_cpf": row["doctor_cpf"],
            "patient_cpf": row["patient_cpf"],
            "ubs_cnes": row["ubs_cnes"],
            "date": row["appointment_datetime"],  # renomeando
            "id": row["id"],
            "message": "Appointment found."
        })

    # Converte os campos para o schema correto
    return appointments

def select_appointment_id(id: int, session: Session):
    user = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    if user is None:
        return None

    return {
        "doctor_cpf": user["doctor_cpf"],
        "patient_cpf": user["patient_cpf"],
        "ubs_cnes": user["ubs_cnes"],
        "date": user["appointment_datetime"],
        "id": user["id"],
        "message": "Appointment deleted successfully"
    }


def select_all_appointments(session: Session):
    result = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
        """)
        )
        .mappings()
        .fetchall()
    )

    appointments = []
    for row in result:
        appointments.append({
            "doctor_cpf": row["doctor_cpf"],
            "patient_cpf": row["patient_cpf"],
            "ubs_cnes": row["ubs_cnes"],
            "date": row["appointment_datetime"],  # renomeando
            "id": row["id"],
            "message": "Appointment found."
        })

    # Converte os campos para o schema correto
    return appointments

def update_appointment(appointment_info: AppointmentIn, id: int, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
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
            UPDATE "appointment" SET
                doctor_cpf = :doctor_cpf,
                patient_cpf = :patient_cpf,
                ubs_cnes = :ubs_cnes,
                p_datetime = :date

            WHERE id = :id
        """),
        {**appointment_info.model_dump(), 'id': id},
    )

    session.commit()

    updated_user = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
            WHERE id = :id
        """),
            {'id': id},
        )
        .mappings()
        .first()
    )

    return updated_user


def delete_appointment_db(id: int, session: Session):

    user = (
        session.execute(
            text("""
            SELECT * FROM "appointment"
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
            DELETE FROM "appointment"
            WHERE id = :id
        """),
        {'id': id},
    )

    session.commit()

    return {
        "doctor_cpf": user["doctor_cpf"],
        "patient_cpf": user["patient_cpf"],
        "ubs_cnes": user["ubs_cnes"],
        "date": user["appointment_datetime"],   # renomeado
        "id": user["id"],
        "message": "Appointment deleted successfully"
    }

