
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import Application
from schemas.schemas import ApplicationCreate, ApplicationUpdate
from typing import List, Optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import or_, and_

class ApplicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, app_id: int) -> Optional[Application]:
        result = await self.session.execute(select(Application).where(Application.id == app_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Application]:
        result = await self.session.execute(select(Application))
        return result.scalars().all()

    async def create(self, app_in: ApplicationCreate) -> Application:
        app = Application(**app_in.dict())
        self.session.add(app)
        await self.session.commit()
        await self.session.refresh(app)
        return app

    async def update(self, app_id: int, app_in: ApplicationUpdate) -> Optional[Application]:
        result = await self.session.execute(select(Application).where(Application.id == app_id))
        app = result.scalar_one_or_none()
        if app:
            app.title = app_in.title
            app.description = app_in.description
            await self.session.commit()
            await self.session.refresh(app)
        return app

    async def delete(self, app_id: int) -> bool:
        result = await self.session.execute(select(Application).where(Application.id == app_id))
        app = result.scalar_one_or_none()
        if app:
            await self.session.delete(app)
            await self.session.commit()
            return True
        return False