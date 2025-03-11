from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TagBase(BaseModel):
    """
    Base schema for tag data.
    
    Contains fields that are common to both input and output models.
    
    Attributes:
        name: Tag name
    """
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    """
    Schema for creating a new tag.
    
    Identical to TagBase for now, but separated for consistency
    and to allow future extensions.
    """
    pass


class TagUpdate(BaseModel):
    """
    Schema for updating an existing tag.
    
    Attributes:
        name: Updated tag name
    """
    name: str = Field(..., min_length=1, max_length=50)


class TagResponse(TagBase):
    """
    Schema for tag data in API responses.
    
    Extends TagBase with ID field.
    
    Attributes:
        id: Unique identifier
    """
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode for conversion from ORM objects


class TagWithPostCount(TagResponse):
    """
    Enhanced tag response that includes post count.
    
    Extends TagResponse with a count of associated posts.
    
    Attributes:
        post_count: Number of posts associated with this tag
    """
    post_count: int

    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """
    Schema for a list of tags in API responses.
    
    Attributes:
        tags: List of tag objects
        total: Total number of tags
    """
    tags: List[TagResponse]
    total: int


# Recursive tag hierarchy model for potential future use
class TagWithChildren(TagResponse):
    """
    Schema for hierarchical tag structure.
    
    Extends TagResponse with a list of child tags.
    
    Attributes:
        children: List of child tag objects
    """
    children: List['TagWithChildren'] = []

    class Config:
        from_attributes = True


# Resolve forward reference
TagWithChildren.update_forward_refs() 