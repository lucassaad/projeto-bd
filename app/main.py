from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api import user
from app.api import appointment
from app.api import nurse_ubs
from app.api import nurse_specialty
from app.api import patient_ubs
from app.api import nurse
from app.api import patient

from app.api import doctor_specialty
from app.api import doctor_ubs
from app.api import doctor
from app.api import ubs
from app.api import specialty
from app.api import vaccine
from app.api import exam
from app.api import prescription
from app.api import medication_prescription
from app.api import medication
from app.api import detailed_appointments

app = FastAPI()

app.include_router(user.router)
app.include_router(appointment.router)
app.include_router(nurse_ubs.router)
app.include_router(nurse_specialty.router)
app.include_router(patient_ubs.router)
app.include_router(nurse_ubs.router)
app.include_router(nurse.router)
app.include_router(patient.router)
app.include_router(doctor_specialty.router)
app.include_router(doctor_ubs.router)
app.include_router(doctor.router)
app.include_router(ubs.router)
app.include_router(specialty.router)
app.include_router(vaccine.router)
app.include_router(exam.router)
app.include_router(prescription.router)
app.include_router(medication_prescription.router)
app.include_router(medication.router)
app.include_router(detailed_appointments.router)

# Templates
templates = Jinja2Templates(directory="app/templates")

# Static files (css, js, imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Página HTML principal
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Sistema UBS"}
    )

# Endpoint de API (opcional)
@app.get("/api")
def root():
    return {"Project": "Projeto de Banco de Dados"}

# Login page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

# Register page
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )
