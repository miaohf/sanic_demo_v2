"""
Service for user-related business logic.
Implements operations for managing users.
"""
from typing import List, Optional, Dict, Any
from core.logging import Logger
from core.cache import CacheService
from core.events import EventBus, EventType
from repositories.user_repository import UserRepository
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse
from core.pagination import PaginationParams, PaginatedResponse
from core.di import inject

@inject
class UserService:
    """Service for user-related business logic."""
    
    def __init__(
        self,
        user_repository: UserRepository = None,
        logger: Logger = None,
        cache = None,
        event_bus: EventBus = None
    ):
        self.user_repository = user_repository or UserRepository()
        self.logger = logger or app_logger
        self.cache = cache
        self.event_bus = event_bus or event_bus
        
    async def get_all_users(
        self, 
        pagination: PaginationParams
    ) -> PaginatedResponse:
        """
        Get all users with pagination.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            A paginated response with users
        """
        self.logger.info("Getting all users with pagination", 
                        page=pagination.page, 
                        page_size=pagination.page_size)
        
        # 添加对缓存为 None 的检查
        cached_data = None
        if self.cache:
            cache_key = f"users:page:{pagination.page}:size:{pagination.page_size}"
            cached_data = await self.cache.get_json(cache_key)
        
        if cached_data:
            self.logger.info("Returning users from cache", cache_key=cache_key)
            return PaginatedResponse(**cached_data)
            
        # Get from database if not in cache
        result = await self.user_repository.paginate(
            pagination,
            lambda user: UserResponse.model_validate(user).model_dump(mode="json")
        )
        
        # 添加对缓存为 None 的检查
        if self.cache:
            await self.cache.set_json(cache_key, result.model_dump(), ttl=300)  # 5 minutes TTL
        
        return result
        
    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user to get
            
        Returns:
            The user if found, None otherwise
        """
        self.logger.info("Getting user by ID", user_id=user_id)
        
        # 添加对缓存为 None 的检查
        cached_user = None
        if self.cache:
            cache_key = f"user:{user_id}"
            cached_user = await self.cache.get_json(cache_key)
        
        if cached_user:
            self.logger.info("Returning user from cache", user_id=user_id)
            return User(**cached_user)
            
        # Get from database if not in cache
        user = await self.user_repository.get_by_id(user_id)
        
        # 添加对缓存为 None 的检查
        if user and self.cache:
            # Cache the user
            await self.cache.set_json(
                f"user:{user_id}", 
                UserResponse.model_validate(user).model_dump(mode="json"), 
                ttl=600  # 10 minutes TTL
            )
            
        return user
        
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_data: The data for the new user
            
        Returns:
            The created user
        """
        self.logger.info("Creating new user", username=user_data.username)
        
        # Check if user with same username or email already exists
        existing_user = await self.user_repository.get_by_username(user_data.username)
        if existing_user:
            self.logger.warning("Username already taken", username=user_data.username)
            raise ValueError("Username already taken")
            
        existing_email = await self.user_repository.get_by_email(user_data.email)
        if existing_email:
            self.logger.warning("Email already registered", email=user_data.email)
            raise ValueError("Email already registered")
            
        # Create the user
        user = await self.user_repository.create(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,  # In a real app, you'd hash this
            is_active=True
        )
        
        # Publish an event
        await self.event_bus.publish(EventType.USER_CREATED, user)
        
        # Clear user list cache
        await self.cache.delete("users:*")
        
        self.logger.info("User created successfully", user_id=user.id)
        return user
        
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Update an existing user.
        
        Args:
            user_id: The ID of the user to update
            user_data: The new data for the user
            
        Returns:
            The updated user if found, None otherwise
        """
        self.logger.info("Updating user", user_id=user_id)
        
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            self.logger.warning("User not found", user_id=user_id)
            return None
            
        # Check if username is being changed and is already taken
        if user_data.username and user_data.username != user.username:
            existing_user = await self.user_repository.get_by_username(user_data.username)
            if existing_user and existing_user.id != user_id:
                self.logger.warning("Username already taken", username=user_data.username)
                raise ValueError("Username already taken")
                
        # Check if email is being changed and is already registered
        if user_data.email and user_data.email != user.email:
            existing_email = await self.user_repository.get_by_email(user_data.email)
            if existing_email and existing_email.id != user_id:
                self.logger.warning("Email already registered", email=user_data.email)
                raise ValueError("Email already registered")
                
        # Update user fields
        update_data = user_data.model_dump(exclude_unset=True)
        updated_user = await self.user_repository.update(user, **update_data)
        
        # Publish an event
        await self.event_bus.publish(EventType.USER_UPDATED, updated_user)
        
        # Clear user cache
        await self.cache.delete(f"user:{user_id}")
        await self.cache.delete("users:*")
        
        self.logger.info("User updated successfully", user_id=user_id)
        return updated_user
        
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            True if the user was deleted, False otherwise
        """
        self.logger.info("Deleting user", user_id=user_id)
        
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            self.logger.warning("User not found", user_id=user_id)
            return False
            
        # Delete the user
        await self.user_repository.delete(user)
        
        # Publish an event
        await self.event_bus.publish(EventType.USER_DELETED, user_id)
        
        # Clear user cache
        await self.cache.delete(f"user:{user_id}")
        await self.cache.delete("users:*")
        
        self.logger.info("User deleted successfully", user_id=user_id)
        return True 