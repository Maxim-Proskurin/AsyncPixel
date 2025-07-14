import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func
)
from app.core.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    full_name = Column(
        String(100),
        nullable=False
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password = Column(
        String(255),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    