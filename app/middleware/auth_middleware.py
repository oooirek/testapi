# app/middleware/auth_middleware.py

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.db.database import async_session_maker
from app.models.user_model import User  # твоя модель пользователя

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256" 


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        request.state.user = None  # по умолчанию None

        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id: int = payload.get("sub")

                if user_id is not None:
                    async with async_session_maker() as session:
                        user = await session.get(User, user_id)
                        if user:
                            request.state.user = user

            except ExpiredSignatureError:
                return JSONResponse({"detail": "Token expired"}, status_code=401)
            except InvalidTokenError:
                return JSONResponse({"detail": "Invalid token"}, status_code=401)
            except Exception as e:
                print("Auth middleware error:", e)

        # ⚠️ важно: вызов следующего слоя
        response = await call_next(request)
        return response

