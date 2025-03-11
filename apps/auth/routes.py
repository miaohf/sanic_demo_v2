from sanic import Blueprint, json
from sanic.exceptions import Unauthorized

from models.user import User
from schemas.user import UserCreate
from schemas.token import Token
from services.auth import (
    get_password_hash, authenticate_user,
    create_access_token, create_refresh_token, decode_token
)

# Create a blueprint for authentication endpoints
bp = Blueprint('auth', url_prefix='/auth')

@bp.post('/register')
async def register(request):
    """
    Register a new user.
    
    This endpoint creates a new user account and returns authentication tokens.
    
    Request body:
        - username: User's username (required)
        - email: User's email address (required)
        - password: User's password (required)
    
    Returns:
        JSON object containing access and refresh tokens
        400 error if username or email already exists
    """
    data = request.json
    user_data = UserCreate(**data)
    
    # Check if user already exists
    existing_user = await User.filter(username=user_data.username).first() or await User.filter(email=user_data.email).first()
    if existing_user:
        return json({"error": "Username or email already exists"}, status=400)
    
    # Create new user
    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password)
    )
    
    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return json({
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    })

@bp.post('/login')
async def login(request):
    """
    Authenticate a user and issue tokens.
    
    This endpoint verifies credentials and returns authentication tokens.
    
    Request body:
        - username: User's username (required)
        - password: User's password (required)
    
    Returns:
        JSON object containing access and refresh tokens
        401 error if credentials are invalid
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return json({"error": "Please provide username and password"}, status=400)
    
    user = await authenticate_user(username, password)
    if not user:
        return json({"error": "Invalid username or password"}, status=401)
    
    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return json({
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    })

@bp.post('/refresh')
async def refresh_token(request):
    """
    Refresh an access token using a refresh token.
    
    This endpoint issues a new access token when provided with a valid refresh token.
    
    Request body:
        - refresh_token: A valid refresh token (required)
    
    Returns:
        JSON object containing a new access token
        401 error if refresh token is invalid
    """
    data = request.json
    refresh_token = data.get("refresh_token")
    
    if not refresh_token:
        return json({"error": "Please provide refresh token"}, status=400)
    
    payload = decode_token(refresh_token)
    if not payload or "refresh" not in payload:
        return json({"error": "Invalid refresh token"}, status=401)
    
    user_id = int(payload.get("sub"))
    
    # Generate new access token
    new_access_token = create_access_token(user_id)
    
    return json({"access_token": new_access_token, "token_type": "bearer"}) 