"""
Repository for Post data access operations.
Extends the BaseRepository with post-specific operations.
"""
from typing import Optional, List, Callable, Any
from tortoise.expressions import Q
from tortoise.functions import Count

from models.post import Post
from models.tag import Tag
from core.pagination import PaginationParams, PaginatedResponse, paginate_queryset

class PostRepository:
    """Repository for Post data access operations."""
    
    def __init__(self):
        self.model_class = Post
        
    async def get_by_id(self, id: int) -> Optional[Post]:
        """Get a post by ID."""
        return await Post.get_or_none(id=id)
        
    async def get_by_id_with_relations(self, id: int) -> Optional[Post]:
        """Get a post by ID with author and tags."""
        post = await self.get_by_id(id)
        if post:
            await post.fetch_related("author", "tags")
        return post
        
    async def get_all(self) -> List[Post]:
        """Get all posts."""
        return await Post.all()
        
    async def create(self, **kwargs) -> Post:
        """Create a new post."""
        return await Post.create(**kwargs)
        
    async def update(self, instance: Post, **kwargs) -> Post:
        """Update a post."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await instance.save()
        return instance
        
    async def delete(self, instance: Post) -> None:
        """Delete a post."""
        await instance.delete()
        
    async def filter(self, **kwargs) -> List[Post]:
        """Filter posts by criteria."""
        return await Post.filter(**kwargs)
        
    async def add_tags(self, post: Post, tags: List[Tag]) -> None:
        """Add tags to a post."""
        if tags:  # 确保 tags 不是空列表
            await post.tags.add(*tags)
        
    async def remove_tags(self, post: Post, tags: List[Tag]) -> None:
        """Remove tags from a post."""
        await post.tags.remove(*tags)
        
    async def clear_tags(self, post: Post) -> None:
        """Remove all tags from a post."""
        await post.tags.clear()
        
    async def paginate(
        self,
        params: PaginationParams,
        transform_func: Callable[[Post], Any] = None,
        **filters
    ) -> PaginatedResponse:
        """
        Paginate posts with optional filtering.
        
        Args:
            params: Pagination parameters
            transform_func: Optional function to transform each post
            **filters: Filter conditions
            
        Returns:
            Paginated response with posts
        """
        queryset = Post.filter(**filters)
        return await paginate_queryset(queryset, params, transform_func)
        
    async def search(self, query: str) -> List[Post]:
        """
        Search posts by title or content.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching posts
        """
        return await Post.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        
    async def get_by_author_id(self, author_id: int) -> List[Post]:
        """Get all posts by a specific author ID."""
        return await Post.filter(author_id=author_id)
        
    async def get_by_tag_id(self, tag_id: int) -> List[Post]:
        """Get all posts with a specific tag ID."""
        return await Post.filter(tags__id=tag_id)