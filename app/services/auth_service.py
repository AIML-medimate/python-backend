from app.utils import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Patient, Doctor
from app.utils.password import verify_password
from app.utils.model_to_dictionary import model_to_dict
from app.schemas.auth_schema import LoginUser
from app.core.config import setting
from app.core import success_response
from app.core import AppException, NotFoundException


async def signin_user(payload: LoginUser, db: AsyncSession, user_type: str = "patient"):
    """
    Signs in a user (patient or doctor) by verifying their email and password.

    Args:
        payload (LoginUser): The user data containing email and password.
        db (AsyncSession): The asynchronous database session used for querying the database.
        user_type (str): Type of user, either "patient" or "doctor".

    Returns:
        dict: A success response containing the user's data if the credentials are valid.

    Raises:
        NotFoundException: If the user with the given email does not exist or if the password is incorrect.
    """

    if user_type == "patient":
        model = Patient
        role = "patient"
    elif user_type == "doctor":
        model = Doctor
        role = "doctor"
    else:
        raise AppException("Invalid user type")

    result = await db.execute(select(model).where(model.email == payload.email))
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise NotFoundException(f"{user_type.capitalize()} with email {payload.email} not found")

    if not verify_password(payload.password, existing_user.password):
        raise NotFoundException("Incorrect password")

    user_data = model_to_dict(existing_user, exclude=["password"])
    access_token = create_access_token(subject=existing_user.id, role=role)
    user_data["access_token"] = access_token

    return success_response(user_data, message=f"{user_type.capitalize()} signed in successfully")
