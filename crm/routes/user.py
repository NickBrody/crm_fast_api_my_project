from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import UserCreate, UserRolesUpdate
from service.user_service import UserService
from routes.dependencies import get_async_session, get_current_user
from models.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=201)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_async_session)):
    service = UserService(session)
    try:
        user = await service.register_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": user.id, "username": user.username, "email": user.email}


@router.patch("/{user_id}/roles", status_code=200)
async def update_user_roles(
    user_id: int,
    roles_update: UserRolesUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if not any(role.name == "admin" for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    service = UserService(session)
    try:
        user = await service.update_user_roles(user_id, roles_update.role_ids)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"id": user.id, "roles": [role.name for role in user.roles]}
