from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 

from app import get_db
from app.services import get_all_patients,create_new_patient, get_all_blood_reports, add_blood_tests
from app.schemas import PatientCreate,BloodReportCreate
router = APIRouter(tags=["Patient"])

@router.get("/")
async def get_patients(db:AsyncSession = Depends(get_db)):
    return await get_all_patients(db)
    

@router.post("/")
async def createPatient(patient: PatientCreate,db:AsyncSession = Depends(get_db)):
    return await create_new_patient(patient=patient, db = db)

@router.get("/{patient_id}/blood-reports")
async def get_blood_reports(patient_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_all_blood_reports(patient_id=patient_id, db=db)

@router.post("/{patient_id}/blood-reports")
async def add_blood_report(patient_id: UUID, blood_tests: BloodReportCreate, db: AsyncSession = Depends(get_db)):
    return await add_blood_tests(patient_id=patient_id, blood_tests=blood_tests, db=db)