
from fastapi import FastAPI
from models.sqlalchemy import Base
from routes.routes import router as applications_router
from routes.dependencies import engine

app = FastAPI()

