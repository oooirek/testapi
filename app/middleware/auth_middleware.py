from pathlib import Path
from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_session
from app.models.user_model import User
import jwt


# Пути к ключам
BASE_DIR = Path(__file__).resolve().parent.parent.parent
KEYS_DIR = BASE_DIR / "certs"
PUBLIC_KEY_PATH = KEYS_DIR / "jwt-public.pem"

# Читаем публичный ключ
with open(PUBLIC_KEY_PATH, 'r') as f:
    PUBLIC_KEY = f.read()

ALGORITHM = "RS256"

async def verify_user_middleware(request: Request, call_next):
    request.state.user = None  # ← чтобы всегда существовал атрибут
    # Проверяем, начинается ли путь с /tasks
    if request.url.path.startswith("/tasks"):
        token = request.cookies.get("token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        try:
            # Декодируем токен с помощью публичного ключа
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        # Получаем сессию БД
        session_gen = get_session()
        session: AsyncSession = await anext(session_gen)

        try:
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalars().first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            if not user.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User not verified"
                )
            
            request.state.user = user
            
        finally:
            await session_gen.aclose()

    response = await call_next(request)
    return response