import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db import Base


class Task(Base):
    
    __tablename__ = "tasks"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    image_path = Column(
        String(255),
        nullable=False
    )
    status = Column(
        String(50),
        nullable=False,
        default="pending"
    )
    result_path = Column(
        String(255),
        nullable=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    user = relationship(
        "User",
        back_populates="tasks"
    )