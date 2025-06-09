from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import Patient
from app.utils import hash_password,verify_password, model_to_dict
from app.schemas import PatientCreate,BloodReportCreate
from app.core import success_response
from app.core import AppException, NotFoundException


async def get_all_patients(db:AsyncSession):
    """
    This function is used to get all Patients from the Patient Database
    """
    result = await db.execute(select(Patient))
    allPatients = result.scalars().all()
    return success_response(allPatients)

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
    patient.password = hash_password(patient.password)
    
    new_patient = Patient(name=patient.name,email=patient.email,date_of_birth=patient.date_of_birth,password=patient.password)
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    patient_data = model_to_dict(new_patient, exclude=["password"])
    return success_response(patient_data,status_code=201,message="Patient created successfully")