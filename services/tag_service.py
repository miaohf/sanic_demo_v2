"""
Service for tag-related business logic.
Implements operations for managing tags.
"""
from typing import List, Optional, Dict, Any
from tortoise.transactions import atomic

from models.tag import Tag
from schemas.tag import TagCreate, TagUpdate, TagResponse, TagWithPostCount
from core.pagination import PaginationParams, PaginatedResponse
from core.logging import Logger, app_logger
from core.events import EventBus, EventType, event_bus
from repositories.tag_repository import TagRepository
from repositories.post_repository import PostRepository
from core.di import inject

@inject
class TagService:
    """Service for tag-related business logic."""
    
    def __init__(
        self,
        tag_repository: TagRepository = None,
        post_repository: PostRepository = None,
        logger: Logger = None,
        event_bus: EventBus = None
    ):
        # Use injected dependencies or create defaults
        self.tag_repository = tag_repository or TagRepository()
        self.post_repository = post_repository or PostRepository()
        self.logger = logger or app_logger
        self.event_bus = event_bus  # 可以是 None
        
    async def get_all_tags(
        self, 
        pagination: PaginationParams
    ) -> PaginatedResponse:
        """
        Get all tags with pagination.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            A paginated response with tags
        """
        self.logger.info("Getting all tags with pagination", 
                        page=pagination.page, 
                        page_size=pagination.page_size)
        
        # Define a transform function to convert to response
        def transform_tag(tag):
            return TagResponse.model_validate(tag).model_dump(mode="json")
            
        # Get from database
        result = await self.tag_repository.paginate(
            pagination,
            transform_tag
        )
        
        return result
        
    async def get_tag(self, tag_id: int) -> Optional[Tag]:
        """
        Get a tag by ID.
        
        Args:
            tag_id: The ID of the tag to get
            
        Returns:
            The tag if found, None otherwise
        """
        self.logger.info("Getting tag by ID", tag_id=tag_id)
        
        return await self.tag_repository.get_by_id(tag_id)
        
    async def get_tag_with_post_count(self, tag_id: int) -> Optional[Dict]:
        """
        Get a tag by ID with post count.
        
        Args:
            tag_id: The ID of the tag to get
            
        Returns:
            Dict with tag data and post count if found, None otherwise
        """
        self.logger.info("Getting tag with post count", tag_id=tag_id)
        
        return await self.tag_repository.get_with_post_count(tag_id)
        
    async def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """
        Get a tag by name.
        
        Args:
            name: The name of the tag to get
            
        Returns:
            The tag if found, None otherwise
        """
        self.logger.info("Getting tag by name", name=name)
        
        return await self.tag_repository.get_by_name(name)
        
    @atomic()
    async def create_tag(self, tag_data: TagCreate) -> Tag:
        """
        Create a new tag.
        
        Args:
            tag_data: The data for the new tag
            
        Returns:
            The created tag
        """
        self.logger.info("Creating new tag", name=tag_data.name)
        
        # Check if tag with same name already exists
        existing_tag = await self.tag_repository.get_by_name(tag_data.name)
        if existing_tag:
            self.logger.warning("Tag already exists", name=tag_data.name)
            return existing_tag
            
        # Create the tag
        tag = await self.tag_repository.create(name=tag_data.name)
        
        # 添加对 event_bus 为 None 的检查
        if self.event_bus:
            await self.event_bus.publish(EventType.TAG_CREATED, tag.id)
        
        self.logger.info("Tag created successfully", tag_id=tag.id)
        return tag
        
    @atomic()
    async def update_tag(self, tag_id: int, tag_data: TagUpdate) -> Optional[Tag]:
        """
        Update an existing tag.
        
        Args:
            tag_id: The ID of the tag to update
            tag_data: The new data for the tag
            
        Returns:
            The updated tag if successful, None otherwise
        """
        self.logger.info("Updating tag", tag_id=tag_id)
        
        # Get tag
        tag = await self.tag_repository.get_by_id(tag_id)
        if not tag:
            self.logger.warning("Tag not found", tag_id=tag_id)
            return None
            
        # Check if new name already exists
        if tag_data.name != tag.name:
            existing_tag = await self.tag_repository.get_by_name(tag_data.name)
            if existing_tag and existing_tag.id != tag_id:
                self.logger.warning("Tag name already exists", name=tag_data.name)
                raise ValueError("Tag name already exists")
            
        # Update tag
        update_data = tag_data.model_dump(exclude_unset=True)
        tag = await self.tag_repository.update(tag, **update_data)
        
        # 添加对 event_bus 为 None 的检查
        if self.event_bus:
            await self.event_bus.publish(EventType.TAG_UPDATED, tag.id)
        
        self.logger.info("Tag updated successfully", tag_id=tag_id)
        return tag
        
    @atomic()
    async def delete_tag(self, tag_id: int) -> bool:
        """
        Delete a tag.
        
        Args:
            tag_id: The ID of the tag to delete
            
        Returns:
            True if the tag was deleted, False otherwise
        """
        self.logger.info("Deleting tag", tag_id=tag_id)
        
        # Get tag
        tag = await self.tag_repository.get_by_id(tag_id)
        if not tag:
            self.logger.warning("Tag not found", tag_id=tag_id)
            return False
            
        # Delete the tag
        await self.tag_repository.delete(tag)
        
        # 添加对 event_bus 为 None 的检查
        if self.event_bus:
            await self.event_bus.publish(EventType.TAG_DELETED, tag_id)
        
        self.logger.info("Tag deleted successfully", tag_id=tag_id)
        return True
        
    async def get_tag_posts(self, tag_id: int, pagination: PaginationParams) -> Optional[Dict]:
        """
        Get all posts with a specific tag.
        
        Args:
            tag_id: The ID of the tag
            pagination: Pagination parameters
            
        Returns:
            Dict with tag data and paginated posts if found, None otherwise
        """
        self.logger.info("Getting posts for tag", tag_id=tag_id)
        
        # Get tag
        tag = await self.tag_repository.get_by_id(tag_id)
        if not tag:
            self.logger.warning("Tag not found", tag_id=tag_id)
            return None
            
        # Define a transform function for posts
        async def transform_post(post):
            await post.fetch_related("author", "tags")
            return post.model_dump(mode="json")
            
        # Get posts for tag
        posts_queryset = self.post_repository.filter(tags=tag)
        posts_result = await self.post_repository.paginate(
            posts_queryset,
            pagination,
            transform_post
        )
        
        # Create response
        result = {
            "tag": TagResponse.model_validate(tag).model_dump(mode="json"),
            "posts": posts_result.model_dump(mode="json")
        }
        
        return result