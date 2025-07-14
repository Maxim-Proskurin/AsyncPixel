from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user