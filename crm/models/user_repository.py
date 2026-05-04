from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User, Role
from schemas.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str):
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate):
        hashed_password = pwd_context.hash(user_in.password)
        user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_roles(self, user_id: int, role_ids: list):
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        roles_result = await self.session.execute(select(Role).where(Role.id.in_(role_ids)))
        roles = roles_result.scalars().all()
        user.roles = roles
        await self.session.commit()
        await self.session.refresh(user)
        return user
