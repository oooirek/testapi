from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.models import User
from app.auth.utils import verify_password, get_password_hash

"""функции работы с БД: создание пользователя, поиск по email, проверка пароля."""



async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, email: str, password: str):
    user = User(email=email, hashed_password=get_password_hash(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
