from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import BloodReport, Patient, Doctor
from app.utils import model_to_dict
from app.schemas import BloodReportCreate
from app.core import success_response
from app.core import AppException, NotFoundException


async def get_all_blood_reports(patient_id:UUID,db: AsyncSession):
    """
    This function retrieves all blood reports for a specific patient.
    """
    result = await db.execute(select(BloodReport).where(BloodReport.patient_id == patient_id))
    allBloodReports = result.scalars().all()
    serialized_reports = [model_to_dict(report) for report in allBloodReports]
    return success_response(serialized_reports,message="Blood reports retrieved successfully")

async def add_blood_tests(doctor_id: UUID, blood_test: BloodReportCreate, db: AsyncSession):
    """
    Adds new blood tests for a specific doctor.

    Args:
        doctor_id (UUID): The ID of the doctor who is adding blood tests.
        blood_test (BloodReportCreate): The blood test results to be added.
        db (AsyncSession): The asynchronous database session used for committing the updates.
    
    Returns:
        message (dict): A success response containing a message indicating the blood tests were added successfully.
    
    Raises:
        NotFoundException: If the doctor with the given ID does not exist.
    """
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    result = await db.execute(select(Patient).where(Patient.id == blood_test.patient_id))
    patient = result.scalar_one_or_none()

    if not patient:
        raise NotFoundException(f"Patient with id {blood_test.patient_id} not found")

    if not doctor:
        raise NotFoundException(f"Doctor with id {doctor_id} not found")

    new_report = BloodReport(
        patient_id=patient.id,
        observed_date=blood_test.observed_date,
        result=blood_test.result
    )
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)

    return success_response(message="Blood tests added successfully")