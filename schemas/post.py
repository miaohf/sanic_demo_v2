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
    title: str = Field(..., min_length=1, max_length=255)
    content: str


class PostCreate(PostBase):
    tags: Optional[List[str]] = None


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True 