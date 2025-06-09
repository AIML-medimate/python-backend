from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import date
class BloodReport(BaseModel):
    observed_date : date
    result: str

class BloodReportCreate(BloodReport):
    pass

