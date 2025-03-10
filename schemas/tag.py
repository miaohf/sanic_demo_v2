from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TagBase(BaseModel):
    """标签基础模型"""
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    """创建标签的请求模型"""
    pass


class TagUpdate(BaseModel):
    """更新标签的请求模型"""
    name: str = Field(..., min_length=1, max_length=50)


class TagResponse(TagBase):
    """标签响应模型"""
    id: int

    class Config:
        from_attributes = True


class TagWithPostCount(TagResponse):
    """包含文章数量的标签响应模型"""
    post_count: int

    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """标签列表响应模型"""
    tags: List[TagResponse]
    total: int


# 递归标签关系模型，用于展示标签层次结构（如果将来需要）
class TagWithChildren(TagResponse):
    """包含子标签的标签层次结构"""
    children: List['TagWithChildren'] = []

    class Config:
        from_attributes = True


# 解决递归引用
TagWithChildren.update_forward_refs() 