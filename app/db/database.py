
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from fastapi import Depends

from sqlalchemy.orm import DeclarativeBase



engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



async def get_session():
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]





class Base(DeclarativeBase):
    pass