from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends


from fastapi import Depends
from app.db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repository import TaskRepository
from app.schemas.schemas import TaskCreate


router = APIRouter(
    prefix="/tasks_v1",
    tags=["Таски"],
)

@router.post("")
async def add_task(
    task_create: TaskCreate,
    session: AsyncSession = Depends(get_async_session)
    ):
    task = await TaskRepository.create_task(session, title=task_create.title, description=task_create.description)
    return task


@router.get("")
async def get_all_task():
    ...


@router.get("/{task_id}")
async def get_tasks(task_id: int,  session: AsyncSession = Depends(get_async_session)):
    task = await TaskRepository.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, delail= "Task not found")
    return task


@router.patch("")
async def patch_task():
    ...

@router.delete("")
async def patch_task():
    ...

 




