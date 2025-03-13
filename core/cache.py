"""
Caching system for the application.
Provides an interface for caching data with different backends.
"""
import json
import asyncio
from typing import Any, Dict, Optional, Union, TypeVar, Generic, Type
from abc import ABC, abstractmethod
import time

T = TypeVar('T')

class CacheBackend(ABC):
    """Abstract base class for cache backends."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """Get a value from the cache."""
        pass
        
    @abstractmethod
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Set a value in the cache with optional TTL in seconds."""
        pass
        
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        pass
        
    @abstractmethod
    async def clear(self) -> None:
        """Clear all values from the cache."""
        pass

class InMemoryCacheBackend(CacheBackend):
    """In-memory implementation of the cache backend."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Union[str, float]]] = {}
        self._cleaner_task = None
        self._start_cleaner()
        
    def _start_cleaner(self):
        """Start the background task to clean expired cache items."""
        async def cleaner():
            while True:
                await asyncio.sleep(60)  # Run every minute
                self._clean_expired()
                
        self._cleaner_task = asyncio.create_task(cleaner())
        
    def _clean_expired(self):
        """Remove expired items from the cache."""
        now = time.time()
        keys_to_delete = []
        
        for key, item in self._cache.items():
            expires_at = item.get('expires_at')
            if expires_at and expires_at <= now:
                keys_to_delete.append(key)
                
        for key in keys_to_delete:
            del self._cache[key]
            
    async def get(self, key: str) -> Optional[str]:
        """Get a value from the cache."""
        item = self._cache.get(key)
        
        if not item:
            return None
            
        expires_at = item.get('expires_at')
        if expires_at and expires_at <= time.time():
            await self.delete(key)
            return None
            
        return item['value']
        
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Set a value in the cache with optional TTL in seconds."""
        item = {'value': value}
        
        if ttl:
            item['expires_at'] = time.time() + ttl
            
        self._cache[key] = item
        
    async def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        if key in self._cache:
            del self._cache[key]
            
    async def clear(self) -> None:
        """Clear all values from the cache."""
        self._cache.clear()

class CacheService:
    """Service for interacting with the cache."""
    
    def __init__(self, backend: CacheBackend):
        self.backend = backend
        
    async def get(self, key: str) -> Optional[str]:
        """Get a string value from the cache."""
        return await self.backend.get(key)
        
    async def get_json(self, key: str) -> Optional[Dict]:
        """Get a JSON value from the cache and deserialize it."""
        data = await self.backend.get(key)
        if data:
            return json.loads(data)
        return None
        
    async def get_object(self, key: str, model_type: Type[T]) -> Optional[T]:
        """Get a JSON value from the cache and convert it to a Pydantic model."""
        data = await self.get_json(key)
        if data:
            return model_type(**data)
        return None
        
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Set a string value in the cache."""
        await self.backend.set(key, value, ttl)
        
    async def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Serialize a value to JSON and store it in the cache."""
        json_data = json.dumps(value)
        await self.backend.set(key, json_data, ttl)
        
    async def set_object(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Serialize a Pydantic model to JSON and store it in the cache."""
        if hasattr(value, 'model_dump'):
            json_data = json.dumps(value.model_dump())
        else:
            json_data = json.dumps(value)
        await self.backend.set(key, json_data, ttl)
        
    async def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        await self.backend.delete(key)
        
    async def clear(self) -> None:
        """Clear all values from the cache."""
        await self.backend.clear() 