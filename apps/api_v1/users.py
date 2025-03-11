from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized

from models.user import User
from schemas.user import UserUpdate, UserResponse

# Create a blueprint for user-related endpoints
bp = Blueprint('users_v1', url_prefix='/users')

@bp.get('/')
async def get_users(request):
    """
    Retrieve all users.
    
    This endpoint returns a list of all users in the system.
    Authentication is required.
    
    Returns:
        JSON array of user objects
    """
    users = await User.all()
    user_data = [UserResponse.model_validate(user).model_dump(mode='json') for user in users]
    return json(user_data)

@bp.get('/<user_id:int>')
async def get_user(request, user_id: int):
    """
    Retrieve a specific user by ID.
    
    Path parameters:
        - user_id: The ID of the user to retrieve
    
    Returns:
        JSON object containing the user data
        404 error if user doesn't exist
    """
    user = await User.get_or_none(id=user_id)
    if not user:
        raise NotFound("User not found")
    
    user_data = UserResponse.model_validate(user)
    return json(user_data.model_dump(mode='json'))

@bp.put('/me')
async def update_user(request):
    """
    Update the authenticated user's profile.
    
    This endpoint updates the current user's information.
    Authentication is required.
    
    Request body:
        - username: Updated username (optional)
        - email: Updated email (optional)
        - password: New password (optional)
    
    Returns:
        JSON object containing the updated user data
        401 error if not authenticated
    """
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    user = await User.get_or_none(id=user_id)
    if not user:
        raise NotFound("User not found")
    
    data = request.json
    user_data = UserUpdate(**data)
    
    # Update user information
    update_data = user_data.model_dump(exclude_unset=True)
    if "password" in update_data:
        from services.auth import get_password_hash
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    await User.filter(id=user_id).update(**update_data)
    
    # Get updated user
    user = await User.get(id=user_id)
    user_data = UserResponse.model_validate(user)
    
    return json(user_data.model_dump(mode='json'))

@bp.get('/me')
async def get_my_info(request):
    """
    Retrieve the authenticated user's profile.
    
    This endpoint returns the current user's information.
    Authentication is required.
    
    Returns:
        JSON object containing the user data
        401 error if not authenticated
    """
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    user = await User.get_or_none(id=user_id)
    if not user:
        raise NotFound("User not found")
    
    user_data = UserResponse.model_validate(user)
    return json(user_data.model_dump(mode='json')) 