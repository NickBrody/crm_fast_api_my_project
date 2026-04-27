from models.sqlalchemy import ApplicationRepository
from schemas.schemas import ApplicationCreate, ApplicationUpdate

class ApplicationService:
    def __init__(self, session):
        self.repo = ApplicationRepository(session)

    async def get_all(self):
        return await self.repo.get_all()

    async def get(self, app_id: int):
        return await self.repo.get(app_id)

    async def create(self, app_in: ApplicationCreate):
        return await self.repo.create(app_in)

    async def update(self, app_id: int, app_in: ApplicationUpdate):
        return await self.repo.update(app_id, app_in)

    async def delete(self, app_id: int):
        return await self.repo.delete(app_id)
