from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import date
class BloodReport(BaseModel):
    patient_id: UUID
    observed_date : date
    result: str

class BloodReportCreate(BloodReport):
    pass

