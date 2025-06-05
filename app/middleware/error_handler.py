from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core import AppException
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

def add_global_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "data": exc.data,
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "data": None,
            }
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": "Conflict: resource already exists",
                "data": None,
            }
        )

    @app.exception_handler(OperationalError)
    async def db_operational_error_handler(request: Request, exc: OperationalError):
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "message": "Database connection error",
                "data": None,
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "data": None,
            }
        )
