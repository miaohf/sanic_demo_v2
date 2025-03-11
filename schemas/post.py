from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class TagResponse(TagBase):
    id: int

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    """
    Base schema for post data.
    
    Contains fields that are common to both input and output models.
    
    Attributes:
        title: Post title
        content: Post content text
    """
    title: str = Field(..., min_length=1, max_length=255)
    content: str


class PostCreate(PostBase):
    """
    Schema for creating a new post.
    
    Extends PostBase with optional tags field.
    
    Attributes:
        tags: List of tag IDs to associate with the post
    """
    tags: Optional[List[int]] = None


class PostUpdate(BaseModel):
    """
    Schema for updating an existing post.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        title: Updated post title (optional)
        content: Updated post content (optional)
        tags: Updated list of tag IDs (optional)
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    tags: Optional[List[int]] = None


class PostResponse(PostBase):
    """
    Schema for post data in API responses.
    
    Extends PostBase with additional read-only fields.
    
    Attributes:
        id: Unique identifier
        created_at: Post creation timestamp
        updated_at: Post last update timestamp
        author_id: ID of the post author
        tags: List of associated tags
    """
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int
    tags: List['TagResponse'] = []

    class Config:
        from_attributes = True  # Enable ORM mode for conversion from ORM objects

# Import here to avoid circular imports
from .tag import TagResponse 