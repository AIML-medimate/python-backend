from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import database as db
from app.routes import patient_route, doctor_route,auth_route
from app import models #imported just to register the tables
from app.middleware import add_global_exception_handlers, FileHandlingMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan,title="Medimate Backend", description="API for predicting cervical cancer using image analysis", version="1.0.0")

add_global_exception_handlers(app)
app.add_middleware(FileHandlingMiddleware)


@app.get("/")
def root_route():
    return {"message":"Hello, World!"}

app.include_router(patient_route.router,prefix="/patients")
app.include_router(doctor_route.router,prefix="/doctors")
app.include_router(auth_route.router,prefix="/auth")