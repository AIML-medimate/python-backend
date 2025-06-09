from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 

from app import get_db
from app.services import get_all_doctors,create_new_doctor
from app.schemas import DoctorCreate
router = APIRouter(tags=["Doctor"])

@router.get("/")
async def get_doctors(db:AsyncSession = Depends(get_db)):
    return await get_all_doctors(db)
    

@router.post("/")
async def createDoctor(doctor: DoctorCreate,db:AsyncSession = Depends(get_db)):
    return await create_new_doctor(doctor=doctor, db = db)