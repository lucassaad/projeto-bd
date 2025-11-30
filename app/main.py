from fastapi import FastAPI

from app.api import user
from app.api import appointment

app = FastAPI()

app.include_router(user.router)
app.include_router(appointment.router)


@app.get('/')
def root():
    return {'Project': 'Projeto de Banco de Dados'}
