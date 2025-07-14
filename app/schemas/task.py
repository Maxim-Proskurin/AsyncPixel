import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TaskBase(BaseModel):
    image_path: str

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    result_path: str | None = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)