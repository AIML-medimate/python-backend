from pydantic import BaseModel
from datetime import date
class DoctorBase(BaseModel):
    name:str
    email:str
    date_of_birth : date
    password: str
    image: str | None = None
    bio : str | None = None

class DoctorCreate(DoctorBase):
    pass

