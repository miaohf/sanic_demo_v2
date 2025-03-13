"""
Base repository class for data access operations.
Provides common CRUD operations for all models.
"""
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from tortoise.models import Model
from tortoise.queryset import QuerySet
from tortoise.exceptions import DoesNotExist
from core.pagination import PaginationParams, paginate_queryset, PaginatedResponse

T = TypeVar('T', bound=Model)

class BaseRepository(Generic[T]):
    """Base repository for data access operations."""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        
    async def get_by_id(self, id: int) -> Optional[T]:
        """Get a model instance by ID."""
        try:
            return await self.model_class.get(id=id)
        except DoesNotExist:
            return None
            
    async def get_all(self) -> List[T]:
        """Get all model instances."""
        return await self.model_class.all()
        
    async def create(self, **kwargs) -> T:
        """Create a new model instance."""
        return await self.model_class.create(**kwargs)
        
    async def update(self, instance: T, **kwargs) -> T:
        """Update a model instance."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await instance.save()
        return instance
        
    async def delete(self, instance: T) -> None:
        """Delete a model instance."""
        await instance.delete()
        
    async def delete_by_id(self, id: int) -> bool:
        """Delete a model instance by ID."""
        instance = await self.get_by_id(id)
        if instance:
            await self.delete(instance)
            return True
        return False
        
    async def count(self) -> int:
        """Count all model instances."""
        return await self.model_class.all().count()
        
    async def exists(self, **kwargs) -> bool:
        """Check if a model instance exists with the given criteria."""
        return await self.model_class.filter(**kwargs).exists()
        
    async def paginate(
        self, 
        params: PaginationParams,
        transform_func = None,
        **filters
    ) -> PaginatedResponse:
        """
        Paginate model instances with optional filtering.
        
        Args:
            params: Pagination parameters
            transform_func: Optional function to transform each item
            **filters: Filter conditions for the queryset
            
        Returns:
            A paginated response with items and page information
        """
        queryset = self.model_class.filter(**filters)
        return await paginate_queryset(queryset, params, transform_func)
        
    def filter(self, **kwargs) -> QuerySet[T]:
        """Get a filtered queryset."""
        return self.model_class.filter(**kwargs) 