from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized
from sanic.request import Request

from services.user_service import UserService
from schemas.user import UserUpdate, UserResponse
from core.pagination import PaginationParams
from core.di import inject
from repositories.user_repository import UserRepository
from core.logging import app_logger
from core.events import event_bus

# Create a blueprint for user-related endpoints
bp = Blueprint('users_v1', url_prefix='/users')

# Initialize services using dependency injection
user_repository = UserRepository()
user_service = UserService(
    user_repository=user_repository,
    logger=app_logger,
    cache=None,  # 或提供一个实际的缓存实现
    event_bus=event_bus
)

@bp.get('/')
async def get_users(request: Request):
    """
    Retrieve all users with pagination.
    
    This endpoint returns a list of all users in the system.
    Authentication is required.
    
    Query parameters:
        - page: Page number (default: 1)
        - page_size: Items per page (default: 10, max: 100)
    
    Returns:
        JSON array of user objects
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Get pagination parameters from query string
    page = int(request.args.get('page', 1))
    page_size = min(int(request.args.get('page_size', 10)), 100)
    pagination = PaginationParams(page=page, page_size=page_size)
    
    # Get users using the service
    result = await user_service.get_all_users(pagination)
    
    return json(result.model_dump(mode='json'))


@bp.get('/<user_id:int>')
async def get_user(request: Request, user_id: int):
    """
    Retrieve a specific user by ID.
    
    Path parameters:
        - user_id: The ID of the user to retrieve
    
    Returns:
        JSON object containing the user data
        404 error if user doesn't exist
    """
    # Get user using the service
    user = await user_service.get_user(user_id)
    
    if not user:
        raise NotFound("User not found")
    
    # Convert to response format
    user_response = UserResponse.model_validate(user)
    return json(user_response.model_dump(mode='json'))


@bp.get('/me')
async def get_current_user(request: Request):
    """
    Retrieve the currently authenticated user.
    
    This endpoint returns the user data for the authenticated user.
    Authentication is required.
    
    Returns:
        JSON object containing the user data
        401 error if not authenticated
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Get user using the service
    user = await user_service.get_user(user_id)
    
    if not user:
        raise NotFound("User not found")
    
    # Convert to response format
    user_response = UserResponse.model_validate(user)
    return json(user_response.model_dump(mode='json'))


@bp.put('/me')
async def update_current_user(request: Request):
    """
    Update the currently authenticated user.
    
    This endpoint updates the user data for the authenticated user.
    Authentication is required.
    
    Request body:
        - username: Updated username (optional)
        - email: Updated email (optional)
    
    Returns:
        JSON object containing the updated user data
        401 error if not authenticated
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Validate request data
    user_data = UserUpdate(**request.json)
    
    # Update user using the service
    updated_user = await user_service.update_user(user_id, user_data)
    
    if not updated_user:
        raise NotFound("User not found")
    
    # Convert to response format
    user_response = UserResponse.model_validate(updated_user)
    return json(user_response.model_dump(mode='json')) 