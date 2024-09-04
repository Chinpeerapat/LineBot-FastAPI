import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from backend.fastapi.dependencies.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line_id = Column(String, unique=True, nullable=False)
    user_name = Column(String, nullable=False)
    pictureUrl = Column(String, nullable=True)
    statusMessage = Column(String, nullable=True) 
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    messages = relationship("Message", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, line_id={self.line_id}, username={self.username})>"