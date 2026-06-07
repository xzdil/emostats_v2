from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from .variables import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# Настройка хеширования паролей (bcrypt — один из самых надёжных алгоритмов)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли введённый пароль с хешем в базе"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хеширует пароль для сохранения в базу"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Создаёт JWT токен с данными из data"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    """Декодирует токен и возвращает payload, если подпись верна"""
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError as e:
        print(f"Error decoding token {token}: {e}")
        return None
