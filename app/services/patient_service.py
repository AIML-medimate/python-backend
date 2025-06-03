from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Patient
from schemas import PatientCreate


async def get_all_patients(db:AsyncSession):
    """
    This function is used to get all Patients from the Patient Database
    """
    result = await db.execute(select(Patient))
    allPatients = result.scalars().all()
    return allPatients

async def create_new_patient(patient: PatientCreate,db:AsyncSession):
    """
    Asynchronously creates a new patient record in the database.
    Args:
        patient (PatientCreate): The patient data to be created, including name, email, and date of birth.
        db (AsyncSession): The asynchronous database session used for committing the new patient.
    Returns:
        Patient: The newly created patient instance with updated fields from the database.
    Raises:
        SQLAlchemyError: If there is an error during the database transaction.
    """
    try:
        new_patient = Patient(name=patient.name,email=patient.email,date_of_birth=patient.date_of_birth)
        db.add(new_patient)
        await db.commit()
        await db.refresh(new_patient)
        return new_patient
    except Exception as e:
        return {"msg":"error while creating Patient","error":e}