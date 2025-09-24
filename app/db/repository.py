
from sqlalchemy import select
from app.models.task_model import Task
from app.db.database import AsyncSession

from app.schemas.schemas import TaskUpdate


class TaskRepository:

    @staticmethod
    async def create_task(session: AsyncSession, title: str, description: str = "") -> Task:
        task = Task(title=title, description=description)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task



    @staticmethod
    async def get_task_by_id(session: AsyncSession, task_id: int):
        stmt = select(Task).where(Task.id == task_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()



    @staticmethod
    async def get_all_tasks(session: AsyncSession):
        result = await session.execute(select(Task))
        return result.scalars().all()



    @staticmethod
    async def update_task(session: AsyncSession, task_id: int, data: TaskUpdate):
        task = await session.get(Task, task_id)
        if not task:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(task, field, value)

        await session.commit()
        await session.refresh(task)
        return task



    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int):
        task = await session.get(Task, task_id)
        if not task:
            return False
        await session.delete(task)
        await session.commit()
        return True


    