from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import Doctor,Patient,BloodReport
from uuid import UUID

from app.schemas import BloodReportCreate
from app.utils import hash_password,verify_password, model_to_dict
from app.schemas import DoctorCreate
from app.core import success_response
from app.core import AppException, NotFoundException


async def get_all_doctors(db:AsyncSession):
    """
    This function is used to get all Doctors from the Doctor Database
    """
    result = await db.execute(select(Doctor))
    allDoctors = result.scalars().all()
    return success_response(allDoctors)

async def create_new_doctor(doctor: DoctorCreate,db:AsyncSession):
    """
    Asynchronously creates a new doctor record in the database.
    Args:
        doctor (DoctorCreate): The doctor data to be created, including name, email, and date of birth.
        db (AsyncSession): The asynchronous database session used for committing the new doctor.
    Returns:
        Doctor: The newly created doctor instance with updated fields from the database.
    Raises:
        SQLAlchemyError: If there is an error during the database transaction.
    """
    doctor.password = hash_password(doctor.password)
    new_doctor = Doctor(name=doctor.name,email=doctor.email,password=doctor.password)
    db.add(new_doctor)
    await db.commit()
    await db.refresh(new_doctor)
    doctor_data = model_to_dict(new_doctor, exclude=["password"])
    return success_response(doctor_data,status_code=201,message="Doctor created successfully")

