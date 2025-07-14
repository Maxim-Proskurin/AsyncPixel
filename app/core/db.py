import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from typing import AsyncGenerator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

ASYNC_DATABASE_URL = DATABASE_URL.replace(
    "postgresql+psycopg2://",
    "postgresql+asyncpg://"
) if DATABASE_URL else ""

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    future=True
    )

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
    )

Base = declarative_base()

async def get_bd() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session