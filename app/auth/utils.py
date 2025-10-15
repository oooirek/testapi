import bcrypt
import jwt
from datetime import datetime, timedelta


from pathlib import Path

# вычисляем путь к папке src, где лежат ключи
BASE_DIR = Path(__file__).resolve().parent.parent.parent  
KEYS_DIR = BASE_DIR / "certs"

PRIVATE_KEY_PATH = KEYS_DIR / "jwt-private.pem"
PUBLIC_KEY_PATH = KEYS_DIR / "jwt-public.pem"

try:
    PRIVATE_KEY = PRIVATE_KEY_PATH.read_text()
    PUBLIC_KEY = PUBLIC_KEY_PATH.read_text()
except FileNotFoundError:
    raise RuntimeError(f"❌ RSA ключи не найдены. Ожидались по пути: {KEYS_DIR}")




ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60





def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())



def create_gvt(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

def decode_gvt(token: str):
    try:
        return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None

