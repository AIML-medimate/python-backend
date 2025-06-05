from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 

from app import get_db
from app.services import get_all_patients,create_new_patient
from app.schemas import PatientCreate
router = APIRouter(tags=["Patient"])

@router.get("/")
async def get_patients(db:AsyncSession = Depends(get_db)):
    return await get_all_patients(db)
    

@router.post("/")
async def createPatient(patient: PatientCreate,db:AsyncSession = Depends(get_db)):
    return await create_new_patient(patient=patient, db = db)