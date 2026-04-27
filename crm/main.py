
from fastapi import FastAPI
from models.models import Base
from routes.routes import router as applications_router
from routes.dependencies import engine

app = FastAPI()
app.include_router(applications_router)

