from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    UploadFile,
    File,
    Response
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.core.db import get_bd
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskRead, TaskBase
from uuid import UUID
import os
import uuid
import shutil

router = APIRouter(prefix="/tasks", tags=["task"])
UPLOAD_DIR = "uploads"

@router.get(
    "/",
    response_model=list[TaskRead]
)
async def get_my_task(
    db: AsyncSession = Depends(get_bd),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
    )
    tasks = result.scalars().all()
    return [TaskRead.model_validate(task) for task in tasks]

@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    task_in: TaskBase,
    db: AsyncSession = Depends(get_bd),
    current_user: User = Depends(get_current_user)
):
    task = Task(
        user_id=current_user.id,
        image_path=task_in.image_path,
        status="pending"
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskRead.model_validate(task)

@router.post(
    "/upload",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED
)
async def upload_task(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_bd),
    current_user: User = Depends(get_current_user)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = file.filename or ""
    file_ext = os.path.splitext(filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при сохранении файла"
        ) from e

    task = Task(
        user_id=current_user.id,
        image_path=file_path,
        status="pending"
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskRead.model_validate(task)
    
@router.get(
    "/{task_id}",
    response_model=TaskRead
)
async def get_task_by_id(
    task_id: UUID,
    db: AsyncSession = Depends(get_bd),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена")
    return TaskRead.model_validate(task)

@router.get(
    "/{task_id}/download",
    response_class=Response
)
async def download_result_file(
    task_id: UUID,
    db: AsyncSession = Depends(get_bd),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    result_path = str(
        getattr(
            task, "result_path",
            None)) if task else None
    if not task or not result_path or not isinstance(
        result_path, 
        str) or not result_path.strip() or not os.path.exists(result_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл результата не найден"
        )
    with open(result_path, "rb") as f:
        data = f.read()
    filename = os.path.basename(result_path)
    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )