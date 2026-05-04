


from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from routes.routes import router as applications_router
from routes.auth import router as auth_router
from routes.user import router as user_router

app = FastAPI()

app.include_router(applications_router)
app.include_router(auth_router)
app.include_router(user_router)

