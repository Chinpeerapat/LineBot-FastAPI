import uuid
from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from backend.fastapi.dependencies.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    message_type = Column(ENUM('user', 'server', name='message_type'), nullable=False)

    # Relationships
    user = relationship("User", back_populates="messages")

    def __repr__(self):
        return (
            f"<Message(id={self.id}, content={self.content}, message_type={self.message_type}, created_at={self.created_at})>"
        )