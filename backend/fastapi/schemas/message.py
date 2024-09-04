from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class MessageBase(BaseModel):
    content: str
    message_type: str

class MessageCreate(MessageBase):
    user_id: UUID

class MessageSchema(MessageBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True