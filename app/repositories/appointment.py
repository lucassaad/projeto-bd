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

    return {"message" : "Appointment created successfully."}
