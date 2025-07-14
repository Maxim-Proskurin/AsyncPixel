import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))


async def get_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str
) -> Optional[User]:
    result = await db.execute(
        select(User)
        .where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, str(user.hashed_password)):
        return None
    return user

def create_access_token(
    data:  dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY не задан в переменных среды!")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    to_encode["type"] = "access"
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY не задан в переменных среды!")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    to_encode["type"] = "refresh"
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

async def create_user(
    db: AsyncSession,
    user_in: UserCreate
) -> tuple[Optional[User], Optional[str]]:
    username_result = await db.execute(
        select(User).where(User.username == user_in.username)
    )
    if username_result.scalar_one_or_none():
        return None, "username"

    email_result = await db.execute(
        select(User).where(User.email == user_in.email)
    )
    if email_result.scalar_one_or_none():
        return None, "email"

    hashed_password = await get_password(user_in.password)
    user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user, None

