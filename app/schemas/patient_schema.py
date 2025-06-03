from pydantic import BaseModel
from datetime import date
class PatientBase(BaseModel):
    name:str
    email:str
    date_of_birth : date

class PatientCreate(PatientBase):
    pass

