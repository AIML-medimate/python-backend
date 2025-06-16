from fastapi import APIRouter, Depends, UploadFile,File,Request
from gradio_client import file
from sqlalchemy.ext.asyncio import AsyncSession 
from uuid import UUID

from app import get_db

from app.services import add_blood_tests
from app.schemas import BloodReportCreate, UserBase,MedicalReportCreate
from app.services import get_all_doctors,create_new_doctor, add_medical_report
from app.dependencies import get_current_user, require_role
from app.core import predict_cervical_cancer,AppException, success_response



router = APIRouter(tags=["Doctor"])

# @router.get("/")
# async def get_doctors(db:AsyncSession = Depends(get_db)):
#     return await get_all_doctors(db)
    


@router.post("/blood-reports")
async def add_blood_report(blood_test: BloodReportCreate, doctor: UserBase = Depends(require_role("doctor")), db: AsyncSession = Depends(get_db)):
    return await add_blood_tests(doctor_id=doctor.sub,blood_test=blood_test, db=db)


@router.post("/medical-reports")
async def create_medical_report(medical_report: MedicalReportCreate, doctor: UserBase = Depends(require_role("doctor")), db: AsyncSession = Depends(get_db)):
    print(doctor)
    return await add_medical_report(
        doctor_id=doctor.sub,
        medical_report=medical_report,
        db=db
    )

@router.post("/diagnose/cervical-cancer")
async def diagnose_cervical_abnormality(request:Request,doctor:UserBase = Depends(require_role("doctor"))):

    file = request.state.uploaded_files.get("file", None)
    if not file:
        raise AppException(
            status_code=400,
            message="No file uploaded. Please upload an image file."
        )
    if not file or not file.filename or not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        raise AppException(
            status_code=400,
            message="Invalid file type. Please upload an image file (PNG, JPG, JPEG, BMP)."
        )

    image_bytes = await file.read()
    label = predict_cervical_cancer(image_bytes)

    return success_response(
        data={"label": label},
        message="Prediction successful"
    )
