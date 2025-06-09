from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import BloodReport, Patient
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

async def add_blood_tests(patient_id: UUID, blood_tests: BloodReportCreate, db: AsyncSession):
    """
    Adds new blood tests for a specific patient.

    Args:
        patient_id (UUID): The ID of the patient whose blood tests are to be added.
        blood_tests (BloodReportCreate): The blood test results to be added.
        db (AsyncSession): The asynchronous database session used for committing the updates.
    
    Returns:
        message (dict): A success response containing a message indicating the blood tests were added successfully.
    
    Raises:
        NotFoundException: If the patient with the given ID does not exist.
    """
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise NotFoundException(f"Patient with id {patient_id} not found")
    
    new_report = BloodReport(
        patient_id=patient.id,
        observed_date=blood_tests.observed_date,
        result=blood_tests.result
    )
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)

    return success_response(message="Blood tests added successfully")