from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
import json
from pydantic import field_validator


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
    
    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, value: Any) -> Optional[List[int]]:
        """将字符串形式的标签数组转换为列表"""
        if value is None:
            return None
            
        # 如果已经是列表，直接返回
        if isinstance(value, list):
            return value
            
        # 如果是字符串形式的数组，尝试解析
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # 如果解析失败，可能是单个值或逗号分隔的字符串
                if ',' in value:
                    # 尝试解析逗号分隔的字符串
                    return [int(tag.strip()) for tag in value.split(',') if tag.strip().isdigit()]
                elif value.strip().isdigit():
                    # 单个数字
                    return [int(value)]
                
        # 返回空列表作为默认值
        return []


class PostUpdate(BaseModel):
    """
    Schema for updating an existing post.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        title: Updated post title (optional)
        content: Updated post content (optional)
        tags: Updated list of tag IDs (optional)
    """
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[int]] = None
    
    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, value: Any) -> Optional[List[int]]:
        """将字符串形式的标签数组转换为列表"""
        if value is None:
            return None
            
        # 如果已经是列表，直接返回
        if isinstance(value, list):
            return value
            
        # 如果是字符串形式的数组，尝试解析
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # 如果解析失败，可能是单个值或逗号分隔的字符串
                if ',' in value:
                    # 尝试解析逗号分隔的字符串
                    return [int(tag.strip()) for tag in value.split(',') if tag.strip().isdigit()]
                elif value.strip().isdigit():
                    # 单个数字
                    return [int(value)]
                
        # 返回空列表作为默认值
        return []


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