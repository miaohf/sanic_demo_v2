"""
Repository for Tag data access operations.
Extends the BaseRepository with tag-specific operations.
"""
from typing import Optional, List, Tuple
from models.tag import Tag
from .base import BaseRepository

class TagRepository(BaseRepository[Tag]):
    """Repository for Tag data access operations."""
    
    def __init__(self):
        super().__init__(Tag)
        
    async def get_by_name(self, name: str) -> Optional[Tag]:
        """Get a tag by name."""
        return await Tag.filter(name=name).first()
        
    async def get_or_create(self, name: str) -> Tuple[Tag, bool]:
        """Get a tag by name or create it if it doesn't exist."""
        tag = await self.get_by_name(name)
        if tag:
            return tag, False
        return await Tag.create(name=name), True
        
    async def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """Get popular tags based on post count."""
        # This requires a custom query or annotation
        # For simplicity, we'll just return all tags for now
        # In a real app, you'd implement a more efficient query
        return await Tag.all().limit(limit)
        
    async def get_with_post_count(self, tag_id: int) -> Optional[dict]:
        """Get a tag with its post count."""
        tag = await self.get_by_id(tag_id)
        if not tag:
            return None
            
        post_count = await tag.posts.all().count()
        tag_dict = {
            "id": tag.id,
            "name": tag.name,
            "post_count": post_count
        }
        return tag_dict 

    async def filter(self, **kwargs) -> List[Tag]:
        """Filter tags by criteria."""
        return await Tag.filter(**kwargs) 