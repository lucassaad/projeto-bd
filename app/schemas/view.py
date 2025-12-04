from pydantic import BaseModel, Field


class ViewBase(BaseModel):
    cpf : str = Field(
        ..., pattern=r'^\d{11}$', description='CPF must contain 11 digits'
    )
    name: str
    email: str
    phone_number: str = Field(..., pattern=r'^\d{10,11}$')
    role: str
    specialty_name  : str | None = None


class ViewIn(ViewBase):
    pass


class ViewOut(ViewBase):
    pass

    
