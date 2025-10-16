from http.client import HTTPException
from fastapi import APIRouter, Depends, Request

from fastapi import Depends
from app.db.database import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repository import TaskRepository
from app.models.task_model import Base
from app.schemas.task_schemas import TaskCreate

from app.db.database import engine



router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

router_1 = APIRouter(
    prefix="/data",
    tags=["database"],
)

@router.post("")
async def add_task(
    request: Request,
    task_create: TaskCreate,
    session: AsyncSession = Depends(get_session)
    ):
    user = request.state.user  # получаем пользователя из мидлвары
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="User not verified")
    
    task = await TaskRepository.create_task(
        session,
        title=task_create.title,
        description=task_create.description,
        user_id=user.id,
        )
    return task


@router.get("")
async def get_all_task(

    session: AsyncSession = Depends(get_session)
    ):
    tasks = await TaskRepository.get_all_tasks(
        session
        )
    return tasks


# починитть рейз
@router.get("/{task_id}")
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    task = await TaskRepository.get_task_by_id(
        session,
        task_id
        )
    if not task:
        raise HTTPException(status_code=404, detail= "Task not found")
    return task


# для галочки готова ли таска
@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    
    task = await TaskRepository.update_task(
        session,
        task_id,
        True
        )
    if not task:
        raise HTTPException(status_code=404, detail= "Task not found")
    return task    


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    task = await TaskRepository.delete_task(
        session,
        task_id
        )
    return {"msg": "success"}






@router_1.post("/setup_db")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"message": "success"}




