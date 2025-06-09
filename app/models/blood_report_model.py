import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime,String, ForeignKey, Text
from datetime import datetime, timezone
from app.database import Base

class BloodReport(Base):
    __tablename__ = "blood_report"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    patient_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("patients.id"))
    observed_date : Mapped[datetime] = mapped_column(DateTime,default=datetime.now(timezone.utc))
    result: Mapped[str] = mapped_column(String(255))