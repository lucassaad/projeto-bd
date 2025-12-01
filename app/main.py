from fastapi import FastAPI

from app.api import user
from app.api import appointment
from app.api import ubs
from app.api import specialty
from app.api import vaccine
from app.api import exam
from app.api import prescription

app = FastAPI()

app.include_router(user.router)
app.include_router(appointment.router)
app.include_router(ubs.router)
app.include_router(specialty.router)
app.include_router(vaccine.router)
app.include_router(exam.router)
app.include_router(prescription.router)

@app.get('/')
def root():
    return {'Project': 'Projeto de Banco de Dados'}
