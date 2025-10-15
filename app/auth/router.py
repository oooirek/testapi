from fastapi import APIRouter, Response
from fastapi.params import Depends


from app.auth.utils import create_gvt
from app.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import RegisterModel, LoginModel
from app.db.repository import AuthRepository



router = APIRouter(
    prefix="/auth",
    tags=["JWT"],
)

# задачи
# разнести логику



@router.post("/register")
async def register(
    data: RegisterModel,
    db: AsyncSession = Depends(get_session)
    ):
    await AuthRepository.register_user(data, db)
    return {"msg": "User registered"}




# делает JWT если юзер зареган и верифицирован
@router.post("/login")
async def login(
    data: LoginModel,
    response: Response,
    db: AsyncSession = Depends(get_session)
    ):
    user = await AuthRepository.authenticate_user(data, db)
    token = create_gvt(user.username)
    response.set_cookie(key="token", value=token, httponly=True)
    return {"msg": "Logged in"}


# проверка верифицирован ли пользователь
# пока что это может сделать и юзер
# но так то должен либо админ либо верификация по почте
@router.post("/verify/{username}")
async def verify_user(
    username: str,
    db: AsyncSession = Depends(get_session)
    ):
    await AuthRepository.verify_user_by_username(username, db)
    return {"msg": f"User {username} verified"}
