from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import (
    appointment,
    doctor,
    nurse,
    patient,
    ubs,
    user,
)

app = FastAPI()

app.include_router(user.router)
app.include_router(appointment.router)
# app.include_router(nurse_ubs.router)
# app.include_router(nurse_specialty.router)
# app.include_router(patient_ubs.router)
# app.include_router(nurse_ubs.router)
app.include_router(nurse.router)
app.include_router(patient.router)
# app.include_router(doctor_specialty.router)
# app.include_router(doctor_ubs.router)
app.include_router(doctor.router)
app.include_router(ubs.router)
# app.include_router(specialty.router)
# app.include_router(vaccine.router)
# app.include_router(exam.router)
# app.include_router(prescription.router)
# app.include_router(medication_prescription.router)
# app.include_router(medication.router)
# app.include_router(detailed_appointments.router)

# Templates
templates = Jinja2Templates(directory='app/templates')

# Static files (css, js, imagens)
app.mount('/static', StaticFiles(directory='app/static'), name='static')


# Página HTML principal
@app.get('/', response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(
        'index.html', {'request': request, 'title': 'Sistema UBS'}
    )


# Endpoint de API (opcional)
@app.get('/api')
def root():
    return {'Project': 'Projeto de Banco de Dados'}


# Login page
@app.get('/login', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


# Register page
@app.get('/register', response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


# Register page
@app.get('/appointments', response_class=HTMLResponse)
def appointments_page(request: Request):
    return templates.TemplateResponse(
        'appointments.html', {'request': request}
    )
