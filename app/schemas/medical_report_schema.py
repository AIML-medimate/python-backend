from uuid import UUID
from pydantic import BaseModel
from datetime import date

class MedicalReport(BaseModel):
    patient_id: UUID
    visiting_date: date
    summary: str
    detailed_description: str

class MedicalReportCreate(MedicalReport):
    pass
