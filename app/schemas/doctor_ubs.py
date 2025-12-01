from datetime import datetime

from pydantic import BaseModel   


class Doctor_ubsBase(BaseModel):
    doctor_cpf: str
    cnes_ubs : str


class Doctor_ubsIn(Doctor_ubsBase):
    pass


class Doctor_ubsOut(Doctor_ubsBase):
    pass


class Doctor_ubsUpdate(Doctor_ubsBase):
    doctor_cpf: str | None = None
    cnes_ubs : str | None = None
    
