from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class ApplicationBase(BaseModel):
    title: str
    description: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- User schemas ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRolesUpdate(BaseModel):
    role_ids: List[int]


class RefreshTokenRequest(BaseModel):
    refresh_token: str
