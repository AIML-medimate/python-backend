from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession 
from typing import Optional, Union
from app.schemas import LoginUser

from app import get_db
from app.services import signin_user, create_new_patient,create_new_doctor
from app.schemas import PatientCreate,DoctorCreate
router = APIRouter(tags=["Authentication"])

@router.post("/register/patient")
async def register_patient(payload: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await create_new_patient(payload, db)

@router.post("/register/doctor")
async def register_doctor(payload: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await create_new_doctor(payload, db)


@router.post("/login/patient")
async def login_patient(payload: LoginUser, db: AsyncSession = Depends(get_db)):
    """
    Endpoint for patient login.
    """
    print("Login payload:", payload)
    return await signin_user(payload, db, user_type="patient")

@router.post("/login/doctor")
async def login_doctor(payload: LoginUser, db: AsyncSession = Depends(get_db)):
    """
    Endpoint for doctor login.
    """
    return await signin_user(payload, db, user_type="doctor")