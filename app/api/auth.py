import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_bd
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user import (authenticate_user, create_access_token,
                               create_refresh_token, create_user)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
bearer_scheme = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["auth"])

async def get_current_user(
    db: AsyncSession = Depends(get_bd),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    if not SECRET_KEY or not ALGORITHM:
        raise credentials_exception
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if not isinstance(user_id, str) or not user_id:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_bd)
) -> UserRead:
    user, error = await create_user(db, user_in)
    if error == "username":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким именем уже существует."
        )
    if error == "email":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует."
        )
    return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_bd)
):
    user = await authenticate_user(
        db,
        form_data.username,
        form_data.password
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
        }
