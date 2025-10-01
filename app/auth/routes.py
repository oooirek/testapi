from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import crud, schemas, jwt_handler, utils
from app.auth.dependencies import get_current_user
from app.db.database import get_session


"""маршруты FastAPI: /register, /login, /refresh, /me."""


router = APIRouter(prefix="/auth", tags=["auth"])




@router.post("/register", response_model=schemas.UserRead)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    existing_user = await crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(400, "User already exists")
    return await crud.create_user(db, user.email, user.password)



@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user_by_email(db, user.email)
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(400, "Invalid credentials")
    access_token = jwt_handler.create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/me", response_model=schemas.UserRead)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user
