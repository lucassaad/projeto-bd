from fastapi import FastAPI

from app.api import user
from app.api import appointment
from app.api import ubs

app = FastAPI()

app.include_router(user.router)
app.include_router(appointment.router)
app.include_router(ubs.router)


@app.get('/')
def root():
    return {'Project': 'Projeto de Banco de Dados'}
