from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    Schema for JWT token response.
    
    This model defines the structure of token responses
    for authentication endpoints.
    
    Attributes:
        access_token: JWT access token string
        refresh_token: JWT refresh token string
        token_type: Token type (always "bearer")
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Schema for JWT token payload.
    
    This model defines the expected structure of the
    decoded JWT token payload.
    
    Attributes:
        sub: Subject identifier (usually user ID)
        exp: Expiration timestamp
    """
    sub: Optional[int] = None
    exp: Optional[int] = None 