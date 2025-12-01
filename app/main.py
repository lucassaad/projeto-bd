from fastapi import FastAPI

from app.api import user
from app.api import appointment
from app.api import nurse_ubs
from app.api import nurse_specialty
from app.api import patient_ubs
from app.api import nurse
from app.api import patient

app = FastAPI()

app.include_router(user.router)
app.include_router(appointment.router)
app.include_router(nurse_ubs.router)
app.include_router(nurse_specialty.router)
app.include_router(patient_ubs.router)
app.include_router(nurse_ubs.router)
app.include_router(nurse.router)
app.include_router(patient.router)


@app.get('/')
def root():
    return {'Project': 'Projeto de Banco de Dados'}
