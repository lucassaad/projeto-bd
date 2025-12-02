from datetime import datetime

from pydantic import BaseModel, Field   


class Doctor_ubsBase(BaseModel):
    doctor_cpf: str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    cnes_ubs : str


class Doctor_ubsIn(Doctor_ubsBase):
    pass


class Doctor_ubsOut(Doctor_ubsBase):
    id: int | None = None
    pass


class Doctor_ubsUpdate(Doctor_ubsBase):
    doctor_cpf: str | None = None
    cnes_ubs : str | None = None
