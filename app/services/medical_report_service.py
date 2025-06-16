from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


from app.models import MedicalReport, Patient,Doctor,Patient
from app.utils import model_to_dict
from app.schemas import MedicalReportCreate
from app.core import success_response
from app.core import AppException, NotFoundException

async def get_latest_medical_reports(patient_id: UUID, doctor_id: Optional[UUID], db: AsyncSession):
    """
    Retrieves the last five medical reports for a specific patient.
    
    Args:
        patient_id (UUID): The ID of the patient whose medical reports are to be retrieved.
        db (AsyncSession): The asynchronous database session used for querying the reports.
    
    Returns:
        dict: A success response containing the last five medical reports for the patient.
    
    Raises:
        NotFoundException: If the patient with the given ID does not exist.
    """
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise NotFoundException(f"Patient with id {patient_id} not found")
    
    # If doctor_id is provided, filter by doctor as well
    if doctor_id is not None:
        result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise NotFoundException(f"Doctor with id {doctor_id} not found")
        
        stmt = (
            select(Patient.name, Doctor.name, MedicalReport.visiting_date, MedicalReport.summary)
            .join(Doctor, MedicalReport.doctor_id == Doctor.id)
            .join(Patient, MedicalReport.patient_id == Patient.id)
            .where(MedicalReport.patient_id == patient_id, MedicalReport.doctor_id == doctor_id)
            .order_by(MedicalReport.visiting_date.desc())
            .limit(5)
        )
    else:
        stmt = (
            select(Patient.name, Doctor.name, MedicalReport.visiting_date, MedicalReport.summary)
            .join(Doctor, MedicalReport.doctor_id == Doctor.id)
            .join(Patient, MedicalReport.patient_id == Patient.id)
            .where(MedicalReport.patient_id == patient_id)
            .order_by(MedicalReport.visiting_date.desc())
        )
    result = await db.execute(stmt)
    medical_reports = result.fetchall()
    
    serialized_reports = [model_to_dict(report) for report in medical_reports]
    return success_response(serialized_reports, message="Latest medical reports retrieved successfully")

async def get_list_of_doctors(patient_id: UUID, db: AsyncSession):
    """
    Retrieves a list of doctors who have created medical reports for a specific patient.
    
    Args:
        patient_id (UUID): The ID of the patient whose doctors are to be retrieved.
        db (AsyncSession): The asynchronous database session used for querying the doctors.
    
    Returns:
        dict: A success response containing the list of doctors for the patient.
    
    Raises:
        NotFoundException: If the patient with the given ID does not exist.
    """
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise NotFoundException(f"Patient with id {patient_id} not found")
    
    stmt = (
        select(Doctor.name, Doctor.id)
        .join(MedicalReport, MedicalReport.doctor_id == Doctor.id)
        .where(MedicalReport.patient_id == patient_id)
        .order_by(MedicalReport.visiting_date.desc())
        .distinct()
    )
    result = await db.execute(stmt)
    doctors = result.fetchall()
    
    serialized_doctors = [model_to_dict(doctor) for doctor in doctors]
    return success_response(serialized_doctors, message="List of doctors retrieved successfully")



async def add_medical_report(doctor_id: UUID, medical_report: MedicalReportCreate, db: AsyncSession):
    """
    Adds a new medical report for a specific patient.
    
    Args:
        patient_id (UUID): The ID of the patient for whom the medical report is being added.
        doctor_id (UUID): The ID of the doctor who created the medical report.
        medical_report (MedicalReportCreate): The medical report data to be added.
        db (AsyncSession): The asynchronous database session used for committing the new report.
    
    Returns:
        dict: A success response indicating that the medical report was added successfully.
    
    Raises:
        NotFoundException: If the patient or doctor with the given IDs does not exist.
    """
    patient_id = medical_report.patient_id
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise NotFoundException(f"Patient with id {patient_id} not found")
    
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    
    if not doctor:
        raise NotFoundException(f"Doctor with id {doctor_id} not found")
    
    new_report = MedicalReport(
        patient_id=patient.id,
        doctor_id=doctor.id,
        visiting_date=medical_report.visiting_date,
        summary=medical_report.summary,
        detailed_description=medical_report.detailed_description
    )

    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    
    return success_response(message="Medical report added successfully")
