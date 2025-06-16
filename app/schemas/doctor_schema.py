from pydantic import BaseModel,EmailStr
class DoctorBase(BaseModel):
    name:str
    email:EmailStr
    password: str
    image: str | None = None
    bio : str | None = None

class DoctorCreate(DoctorBase):
    pass

