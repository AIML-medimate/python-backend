import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date,String
from datetime import date
from app.database import Base
from typing import Optional

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100),unique=True)
    image: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date)

