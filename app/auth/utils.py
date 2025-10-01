from passlib.context import CryptContext

"""(опционально) хэширование паролей, валидации и другие утилиты."""

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    truncated = password.encode("utf-8")[:72]  # ограничение bcrypt в байтах
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(truncated, hashed_password)
