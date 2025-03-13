"""
Repository for User data access operations.
Extends the BaseRepository with user-specific operations.
"""
from typing import Optional, List, Callable, Any
from tortoise.expressions import Q

from models.user import User
from core.pagination import PaginationParams, PaginatedResponse, paginate_queryset

class UserRepository:
    """Repository for User data access operations."""
    
    def __init__(self):
        self.model_class = User
        
    async def get_by_id(self, id: int) -> Optional[User]:
        """Get a user by ID."""
        return await User.get_or_none(id=id)
        
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return await User.filter(username=username).first()
        
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return await User.filter(email=email).first()
        
    async def get_all(self) -> List[User]:
        """Get all users."""
        return await User.all()
        
    async def create(self, **kwargs) -> User:
        """Create a new user."""
        return await User.create(**kwargs)
        
    async def update(self, instance: User, **kwargs) -> User:
        """Update a user."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await instance.save()
        return instance
        
    async def delete(self, instance: User) -> None:
        """Delete a user."""
        await instance.delete()
        
    async def filter(self, **kwargs) -> List[User]:
        """Filter users by criteria."""
        return await User.filter(**kwargs)
        
    async def paginate(
        self,
        params: PaginationParams,
        transform_func: Callable[[User], Any] = None,
        **filters
    ) -> PaginatedResponse:
        """
        Paginate users with optional filtering.
        
        Args:
            params: Pagination parameters
            transform_func: Optional function to transform each user
            **filters: Filter conditions
            
        Returns:
            Paginated response with users
        """
        queryset = User.filter(**filters)
        return await paginate_queryset(queryset, params, transform_func)
        
    async def search(self, query: str) -> List[User]:
        """
        Search users by username or email.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching users
        """
        return await User.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
        
    async def get_active_users(self) -> List[User]:
        """Get all active users."""
        return await User.filter(is_active=True) 