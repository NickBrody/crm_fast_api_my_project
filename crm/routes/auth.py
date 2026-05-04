from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from schemas.schemas import UserLogin
from routes.dependencies import get_async_session
from passlib.context import CryptContext
from sqlalchemy.future import select
from auth.jwt_config import create_access_token, create_refresh_token, decode_refresh_token
from jose import JWTError
from schemas.schemas import RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad username or password")
    return {
        "access_token": create_access_token(subject=db_user.username),
        "refresh_token": create_refresh_token(subject=db_user.username),
        "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh(body: RefreshTokenRequest, session: AsyncSession = Depends(get_async_session)):
    try:
        username = decode_refresh_token(body.refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    result = await session.execute(select(User).where(User.username == username))
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=401, detail="User not found")
    return {
        "access_token": create_access_token(subject=username),
        "token_type": "bearer",
    }
