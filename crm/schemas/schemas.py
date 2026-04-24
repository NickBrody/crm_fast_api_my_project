from pydantic import BaseModel
from typing import Optional

class ApplicationBase(BaseModel):
    title: str
    description: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int

    class Config:
        orm_mode = True
