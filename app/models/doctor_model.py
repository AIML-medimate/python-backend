import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String,Text
from typing import Optional
from app.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100),unique=True)
    image: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    bio : Mapped[Optional[str]] = mapped_column(Text, nullable=True)

