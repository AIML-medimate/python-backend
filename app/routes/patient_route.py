from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession 
from typing import Optional

from app import get_db
from app.services import get_all_patients,create_new_patient, get_all_blood_reports,get_latest_medical_reports
from app.schemas import PatientCreate,BloodReportCreate
from app.dependencies import get_current_user
from app.schemas import UserBase


router = APIRouter(tags=["Patient"])

@router.get("/")
async def get_patients(user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_all_patients(db)
    

@router.get("/blood-reports/{patient_id}")
async def get_blood_reports(patient_id: UUID, user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_all_blood_reports(patient_id=patient_id, db=db)

@router.get("/medical-reports/{patient_id}")
async def get_medical_reports(patient_id: UUID, doctor_id: Optional[UUID] = Query(default=None), user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_latest_medical_reports(patient_id=patient_id, doctor_id=doctor_id, db=db)