
from sqlalchemy import select
from app.models.task_model import Task
from app.db.database import AsyncSession



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
        return await session.get(Task, task_id)



    @staticmethod
    async def get_all_tasks(session: AsyncSession):
        result = await session.execute(select(Task))
        return result.scalars().all()



    @staticmethod
    async def update_task(session: AsyncSession, task_id: int, **kwargs):
        task = await session.get(Task, task_id)
        if not task:
            return None
        for k, v in kwargs.items():
            setattr(task, k, v)
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


    