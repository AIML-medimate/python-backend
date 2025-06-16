from pydantic import BaseModel,EmailStr
from datetime import date
class PatientBase(BaseModel):
    name:str
    email:EmailStr
    date_of_birth : date
    password: str
    image: str | None = None

class PatientCreate(PatientBase):
    pass