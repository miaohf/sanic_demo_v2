"""
Service for post-related business logic.
Implements operations for managing posts.
"""
from typing import List, Optional, Dict, Any
from tortoise.transactions import atomic

from models.post import Post
from models.user import User
from models.tag import Tag
from schemas.post import PostCreate, PostUpdate, PostResponse
from core.pagination import PaginationParams, PaginatedResponse
from core.logging import Logger, app_logger
from core.events import EventBus, EventType, event_bus
from core.cache import CacheService
from repositories.post_repository import PostRepository
from repositories.tag_repository import TagRepository
from repositories.user_repository import UserRepository
from core.di import inject

@inject
class PostService:
    """Service for post-related business logic."""
    
    def __init__(
        self,
        post_repository: PostRepository = None,
        tag_repository: TagRepository = None,
        user_repository: UserRepository = None,
        logger: Logger = None,
        cache_service: CacheService = None,
        event_bus: EventBus = None
    ):
        # Use injected dependencies or create defaults
        self.post_repository = post_repository or PostRepository()
        self.tag_repository = tag_repository or TagRepository()
        self.user_repository = user_repository or UserRepository()
        self.logger = logger or app_logger
        self.cache = cache_service or CacheService(None)  # Default would be set in real app
        self.event_bus = event_bus or event_bus  # Global event bus from core.events
        
    async def get_all_posts(
        self, 
        pagination: PaginationParams
    ) -> PaginatedResponse:
        """
        Get all posts with pagination.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            A paginated response with posts
        """
        self.logger.info("Getting all posts with pagination", 
                        page=pagination.page, 
                        page_size=pagination.page_size)
        
        # Try to get from cache first
        cache_key = f"posts:page:{pagination.page}:size:{pagination.page_size}"
        cached_data = None  # In a real app: await self.cache.get_json(cache_key)
        
        if cached_data:
            self.logger.info("Returning posts from cache", cache_key=cache_key)
            return PaginatedResponse(**cached_data)
            
        # Define a transform function to load relations and convert to response
        async def transform_post(post):
            await post.fetch_related("author", "tags")
            return PostResponse.model_validate(post).model_dump(mode="json")
            
        # Get from database if not in cache
        result = await self.post_repository.paginate(
            pagination,
            transform_post
        )
        
        # Cache the result (in a real app)
        # await self.cache.set_json(cache_key, result.model_dump(), ttl=300)
        
        return result
        
    async def get_post(self, post_id: int) -> Optional[Post]:
        """
        Get a post by ID with all related data.
        
        Args:
            post_id: The ID of the post to get
            
        Returns:
            The post if found, None otherwise
        """
        self.logger.info("Getting post by ID", post_id=post_id)
        
        # Try to get from cache first (in a real app)
        # cache_key = f"post:{post_id}"
        # cached_post = await self.cache.get_json(cache_key)
        
        # Get from database
        post = await self.post_repository.get_by_id_with_relations(post_id)
        
        if post:
            # Cache the post (in a real app)
            # post_data = PostResponse.model_validate(post).model_dump(mode="json")
            # await self.cache.set_json(cache_key, post_data, ttl=600)
            pass
            
        return post
        
    @atomic()
    async def create_post(self, user_id: int, post_data: PostCreate) -> Post:
        """
        Create a new post with optional tags.
        
        Args:
            user_id: The ID of the author
            post_data: The data for the new post
            
        Returns:
            The created post with related data
        """
        self.logger.info("Creating new post", user_id=user_id, title=post_data.title)
        
        # Get user
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            self.logger.error("User not found", user_id=user_id)
            raise ValueError("User not found")
        
        # Create the post
        post = await self.post_repository.create(
            title=post_data.title,
            content=post_data.content,
            author_id=user_id
        )
        
        # Process tags if provided
        if post_data.tags:
            # Get valid tags that match the provided IDs
            valid_tags = await self.tag_repository.filter(id__in=post_data.tags)
            # Associate tags with the post
            await self.post_repository.add_tags(post, valid_tags)
        
        # Load related data
        await post.fetch_related("author", "tags")
        
        # Publish event
        if self.event_bus:
            await self.event_bus.publish(EventType.POST_CREATED, post.id)
        
        # Invalidate cache (in a real app)
        # await self.cache.delete("posts:*")
        
        self.logger.info("Post created successfully", post_id=post.id)
        return post
        
    @atomic()
    async def update_post(
        self, 
        post_id: int, 
        user_id: int, 
        post_data: PostUpdate
    ) -> Optional[Post]:
        """
        Update an existing post.
        
        Args:
            post_id: The ID of the post to update
            user_id: The ID of the user making the request
            post_data: The new data for the post
            
        Returns:
            The updated post if successful, None otherwise
        """
        self.logger.info("Updating post", post_id=post_id, user_id=user_id)
        
        # Get post and verify ownership
        post = await self.post_repository.get_by_id(post_id)
        if not post or post.author_id != user_id:
            self.logger.warning(
                "Post not found or user doesn't have permission",
                post_id=post_id,
                user_id=user_id
            )
            return None
            
        # Update post fields
        update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})
        if update_data:
            post = await self.post_repository.update(post, **update_data)
        
        # Update tags if provided
        if post_data.tags is not None:
            self.logger.debug("Updating post tags", post_id=post_id, tags=post_data.tags)
            
            # 清除现有标签
            await self.post_repository.clear_tags(post)
            
            # 添加新标签
            if post_data.tags:
                tags = await self.tag_repository.filter(id__in=post_data.tags)
                self.logger.debug("Found tags to add", post_id=post_id, tag_count=len(tags))
                await self.post_repository.add_tags(post, tags)
            else:
                self.logger.debug("No tags to add", post_id=post_id)
        
        # Load related data
        await post.fetch_related("author", "tags")
        
        # Publish event
        if self.event_bus:
            await self.event_bus.publish(EventType.POST_UPDATED, post.id)
        
        # Invalidate cache (in a real app)
        # await self.cache.delete(f"post:{post_id}")
        # await self.cache.delete("posts:*")
        
        self.logger.info("Post updated successfully", post_id=post_id)
        return post
        
    @atomic()
    async def delete_post(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post.
        
        Args:
            post_id: The ID of the post to delete
            user_id: The ID of the user making the request
            
        Returns:
            True if the post was deleted, False otherwise
        """
        self.logger.info("Deleting post", post_id=post_id, user_id=user_id)
        
        # Get post and verify ownership
        post = await self.post_repository.get_by_id(post_id)
        if not post or post.author_id != user_id:
            self.logger.warning(
                "Post not found or user doesn't have permission",
                post_id=post_id,
                user_id=user_id
            )
            return False
        
        # Delete the post
        await self.post_repository.delete(post)
        
        # Publish event
        if self.event_bus:
            await self.event_bus.publish(EventType.POST_DELETED, post_id)
        
        # Invalidate cache (in a real app)
        # await self.cache.delete(f"post:{post_id}")
        # await self.cache.delete("posts:*")
        
        self.logger.info("Post deleted successfully", post_id=post_id)
        return True 