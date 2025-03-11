from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    Base schema for user data.
    
    Contains fields that are common to both input and output models.
    
    Attributes:
        username: User's unique username
        email: User's email address
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Extends UserBase with password field for account creation.
    
    Attributes:
        password: User's password (will be hashed before storage)
    """
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        username: Updated username (optional)
        email: Updated email (optional)
        password: New password (optional)
    """
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserBase):
    """
    Schema for user data in API responses.
    
    Extends UserBase with additional read-only fields.
    
    Attributes:
        id: Unique identifier
        is_active: Account status
        created_at: Account creation timestamp
        updated_at: Account last update timestamp
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for conversion from ORM objects