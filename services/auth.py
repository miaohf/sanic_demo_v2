from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from typing import Optional

from config import JWT_SECRET, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await User.get_or_none(username=username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_token(subject: int, expires_delta: Optional[timedelta] = None, is_refresh: bool = False):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + (JWT_REFRESH_TOKEN_EXPIRES if is_refresh else JWT_ACCESS_TOKEN_EXPIRES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    if is_refresh:
        to_encode["refresh"] = True
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_access_token(subject: int):
    return create_token(subject, JWT_ACCESS_TOKEN_EXPIRES)


def create_refresh_token(subject: int):
    return create_token(subject, JWT_REFRESH_TOKEN_EXPIRES, is_refresh=True)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None 