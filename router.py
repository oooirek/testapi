from typing import Annotated
from fastapi import APIRouter, Depends

from repository import TaskRepository
from schemas import STaskAdd, Task, STaskId


router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)

@router.post("")
async def add_task(
    task: Annotated[STaskAdd, Depends()]
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"msg": "success", "task_id": task_id}
    

@router.get("")
async def get_tasks() -> list[Task]:
    tasks = await TaskRepository.find_one()
    return tasks