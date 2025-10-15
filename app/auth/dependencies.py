from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select

from app.auth.utils import decode_gvt
from app.db.database import get_session
from app.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession




async def get_current_user(token: str = Cookie(default=None), db: AsyncSession = Depends(get_session)):
    if not token:
        raise HTTPException(status_code=401, detail="No token")
    payload = decode_gvt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user or not user.is_verified:
        raise HTTPException(status_code=401, detail="User not verified or not found")
    return user