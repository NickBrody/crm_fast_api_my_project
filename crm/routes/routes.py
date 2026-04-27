from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.schemas import Application, ApplicationCreate, ApplicationUpdate
from service.service import ApplicationService
from .dependencies import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/", response_model=List[Application])
async def list_applications(session: AsyncSession = Depends(get_async_session)):
    service = ApplicationService(session)
    return await service.get_all()

@router.post("/", response_model=Application, status_code=201)
async def create_application(app_in: ApplicationCreate, session: AsyncSession = Depends(get_async_session)):
    service = ApplicationService(session)
    return await service.create(app_in)

@router.get("/{app_id}", response_model=Application)
async def get_application(app_id: int, session: AsyncSession = Depends(get_async_session)):
    service = ApplicationService(session)
    app = await service.get(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.put("/{app_id}", response_model=Application)
async def update_application(app_id: int, app_in: ApplicationUpdate, session: AsyncSession = Depends(get_async_session)):
    service = ApplicationService(session)
    app = await service.update(app_id, app_in)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.delete("/{app_id}", status_code=204)
async def delete_application(app_id: int, session: AsyncSession = Depends(get_async_session)):
    service = ApplicationService(session)
    deleted = await service.delete(app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
    return None
