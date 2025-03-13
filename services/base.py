"""
Base service class for business logic operations.
Provides common functionality for all services.
"""
from typing import TypeVar, Generic, Type, Optional
from tortoise import Tortoise
from core.logging import Logger
from core.cache import CacheService
from core.events import EventBus

T = TypeVar('T')

class BaseService:
    """Base service for business logic operations."""
    
    def __init__(
        self,
        logger: Logger,
        cache: CacheService,
        event_bus: EventBus
    ):
        self.logger = logger
        self.cache = cache
        self.event_bus = event_bus
        
    async def transaction(self):
        """Start a database transaction."""
        return Tortoise.get_connection("default").transaction()
        
    async def cache_get(self, key: str, model_type: Optional[Type[T]] = None) -> Optional[T]:
        """Get an item from the cache with optional model conversion."""
        if model_type:
            return await self.cache.get_object(key, model_type)
        return await self.cache.get(key)
        
    async def cache_set(self, key: str, value, ttl: Optional[int] = None) -> None:
        """Set an item in the cache with optional TTL."""
        if hasattr(value, 'model_dump'):
            await self.cache.set_object(key, value, ttl)
        elif isinstance(value, dict):
            await self.cache.set_json(key, value, ttl)
        else:
            await self.cache.set(key, str(value), ttl)
            
    async def cache_delete(self, key: str) -> None:
        """Delete an item from the cache."""
        await self.cache.delete(key)
        
    async def cache_clear(self) -> None:
        """Clear all items from the cache."""
        await self.cache.clear() 