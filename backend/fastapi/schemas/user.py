from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    line_id: str
    user_name: str
    pictureUrl: Optional[str] = None
    statusMessage: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserSchema(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
