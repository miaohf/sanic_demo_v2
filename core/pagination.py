"""
Pagination utilities for the application.
Provides tools for paginating query results.
"""
from typing import TypeVar, Generic, List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field
from tortoise.queryset import QuerySet
import math

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Parameters for pagination."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")

class PageInfo(BaseModel):
    """Information about the current page."""
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_next: bool
    has_previous: bool

class PaginatedResponse(BaseModel, Generic[T]):
    """A response that includes pagination information."""
    items: List[T]
    page_info: PageInfo

async def paginate_queryset(
    queryset: QuerySet,
    params: PaginationParams,
    transform_func = None
) -> PaginatedResponse:
    """
    Paginate a Tortoise ORM QuerySet.
    
    Args:
        queryset: The QuerySet to paginate
        params: The pagination parameters
        transform_func: An optional function to transform each item
        
    Returns:
        A PaginatedResponse with items and page information
    """
    # Get total count for pagination
    total_items = await queryset.count()
    
    # Calculate pagination values
    total_pages = math.ceil(total_items / params.page_size)
    skip = (params.page - 1) * params.page_size
    
    # Get items for current page
    items = await queryset.offset(skip).limit(params.page_size)
    
    # Transform items if a transform function is provided
    if transform_func:
        if callable(transform_func):
            transformed_items = []
            for item in items:
                result = transform_func(item)
                # Handle both regular functions and coroutines
                if hasattr(result, "__await__"):
                    transformed_items.append(await result)
                else:
                    transformed_items.append(result)
        else:
            transformed_items = items
    else:
        transformed_items = items
    
    # Create page info
    page_info = PageInfo(
        total_items=total_items,
        total_pages=total_pages,
        current_page=params.page,
        page_size=params.page_size,
        has_next=params.page < total_pages,
        has_previous=params.page > 1
    )
    
    return PaginatedResponse(
        items=transformed_items,
        page_info=page_info
    ) 