from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.schemas import Application, ApplicationCreate, ApplicationUpdate
from services.service import ApplicationService
from models.sqlalchemy import Application as ApplicationModel
from .dependencies import get_db

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/", response_model=List[Application])
def list_applications(db: Session = Depends(get_db)):
    return ApplicationService.get_all(db)

@router.post("/", response_model=Application, status_code=201)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    return ApplicationService.create(db, app_in)

@router.get("/{app_id}", response_model=Application)
def get_application(app_id: int, db: Session = Depends(get_db)):
    app = ApplicationService.get(db, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.put("/{app_id}", response_model=Application)
def update_application(app_id: int, app_in: ApplicationUpdate, db: Session = Depends(get_db)):
    app = ApplicationService.update(db, app_id, app_in)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.delete("/{app_id}", status_code=204)
def delete_application(app_id: int, db: Session = Depends(get_db)):
    deleted = ApplicationService.delete(db, app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
    return None
