
from fastapi import HTTPException
from sqlalchemy import select
from app.auth.utils import hash_password, verify_password
from app.models.task_model import Task
from app.db.database import AsyncSession

from app.models.user_model import User
from app.schemas.user_schemas import RegisterModel, LoginModel




class TaskRepository:

    @staticmethod
    async def create_task(
        session: AsyncSession,
        title: str,
        user_id: int,
        description: str = ""
        ) -> Task:
        task = Task(title=title, description=description, user_id=user_id)
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
    async def update_task(session: AsyncSession, task_id: int, status: bool):
        task = await session.get(Task, task_id)
        if not task:
            return None
        task.status = status
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




class AuthRepository:


    @staticmethod
    async def register_user(
        data: RegisterModel,
        db: AsyncSession
        ):
        result = await db.execute(select(User).where(User.username == data.username))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Username taken")
        user = User(username=data.username, hashed_password=hash_password(data.password))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


    @staticmethod
    async def authenticate_user(
        data: LoginModel,
        db: AsyncSession
        ):
        result = await db.execute(select(User).where(User.username == data.username))
        user = result.scalars().first()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.is_verified:
            raise HTTPException(status_code=403, detail="User not verified")
        return user


    @staticmethod
    async def verify_user_by_username(
        username: str,
        db: AsyncSession
        ):
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_verified = True
        db.add(user)
        await db.commit()
        return user
    


    