import re
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    
    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError("Пароль должен быть не мене 6 символов.")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Пароль должен иметь хотя бы один спецсимвол.")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну букву.")
        return v
    
class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)