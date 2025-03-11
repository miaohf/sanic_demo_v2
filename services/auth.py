from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from typing import Optional

from config import JWT_SECRET, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES
from models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash.
    
    Args:
        plain_password: The plaintext password to verify
        hashed_password: The stored hash to compare against
    
    Returns:
        bool: True if the password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generate a password hash.
    
    Args:
        password: The plaintext password to hash
    
    Returns:
        str: The generated password hash
    """
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str):
    """
    Authenticate a user by username and password.
    
    Args:
        username: The username to authenticate
        password: The password to verify
    
    Returns:
        User: The authenticated user object, or False if authentication failed
    """
    user = await User.get_or_none(username=username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_token(subject: int, expires_delta: Optional[timedelta] = None, is_refresh: bool = False):
    """
    Create a JWT token.
    
    Args:
        subject: The subject of the token (usually user ID)
        expires_delta: Optional custom expiration time
        is_refresh: Whether this is a refresh token
    
    Returns:
        str: The encoded JWT token
    """
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
    """
    Create an access token for a user.
    
    Args:
        subject: The user ID to create the token for
    
    Returns:
        str: The encoded access token
    """
    return create_token(subject, JWT_ACCESS_TOKEN_EXPIRES)

def create_refresh_token(subject: int):
    """
    Create a refresh token for a user.
    
    Args:
        subject: The user ID to create the token for
    
    Returns:
        str: The encoded refresh token
    """
    return create_token(subject, JWT_REFRESH_TOKEN_EXPIRES, is_refresh=True)

def decode_token(token: str):
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token to decode
    
    Returns:
        dict: The decoded token payload, or None if invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None 