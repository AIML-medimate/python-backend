from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import database as db
from app.routes import patient_route
from app import models #imported just to register the tables

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root_route():
    return {"message":"Hello, World!"}

app.include_router(patient_route.router,prefix="/patients")