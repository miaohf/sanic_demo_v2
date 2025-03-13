from sanic import Request
import jwt
from datetime import datetime
from functools import wraps
from sanic.exceptions import Unauthorized

from config import JWT_SECRET, JWT_ALGORITHM
from services.auth import create_access_token

# Define paths that don't require authentication
PUBLIC_PATHS = [
    "/",
    "/auth/login",
    "/auth/register",
    "/auth/refresh"
]

async def jwt_middleware(request: Request):
    """
    Middleware for JWT authentication.
    
    This middleware processes JWT tokens for authentication:
    1. Skips authentication for public paths
    2. Extracts the Bearer token from Authorization header
    3. Validates the token and extracts user ID
    4. Sets the user ID in request context
    
    Args:
        request: The incoming Sanic request object
    """
    # Skip authentication for public paths
    if request.path in PUBLIC_PATHS:
        return
    
    # Extract token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        request.ctx.user = None
        return
    
    token = auth_header.replace('Bearer ', '')
    
    try:
        # Decode and validate token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Check token expiration
        exp = payload.get('exp')
        if not exp or datetime.now().timestamp() > exp:
            request.ctx.user = None
            return
        
        # Set user ID in request context
        request.ctx.user = int(payload.get('sub'))
        
    except jwt.PyJWTError:
        # Invalid token
        request.ctx.user = None 

def protected():
    """装饰器：确保路由需要认证才能访问"""
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # 验证用户是否已认证
            if not request.ctx.user:
                raise Unauthorized("Please login first")
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator 