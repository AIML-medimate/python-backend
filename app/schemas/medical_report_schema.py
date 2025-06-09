from uuid import UUID
from pydantic import BaseModel
from datetime import date

class MedicalReport(BaseModel):
    id: UUID
    patient_id: UUID
    doctor_id: UUID
    visiting_date: date
    summary: str
    detailed_description: str

class MedicalReportCreate(MedicalReport):
    pass
