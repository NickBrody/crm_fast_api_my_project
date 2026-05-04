from models.user_repository import UserRepository
from schemas.schemas import UserCreate, UserRolesUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register_user(self, user_in: UserCreate):
        existing = await self.repo.get_by_username(user_in.username)
        if existing:
            raise ValueError("Username already exists")
        return await self.repo.create(user_in)

    async def update_user_roles(self, user_id: int, role_ids: list):
        user = await self.repo.update_roles(user_id, role_ids)
        if not user:
            raise ValueError("User not found")
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self.repo.get_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        return user
