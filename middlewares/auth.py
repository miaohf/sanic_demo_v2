from sanic import Request
import jwt
from datetime import datetime

from config import JWT_SECRET, JWT_ALGORITHM
from services.auth import create_access_token

# 不需要验证的路径
PUBLIC_PATHS = [
    "/",
    "/auth/login",
    "/auth/register",
    "/auth/refresh",
]


async def jwt_middleware(request: Request):
    if request.path in PUBLIC_PATHS:
        return
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        request.ctx.user = None
        return
    
    token = auth_header.replace('Bearer ', '')
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # 验证令牌是否过期
        exp = payload.get('exp')
        if not exp or datetime.utcnow().timestamp() > exp:
            request.ctx.user = None
            return
        
        # 保存用户ID到请求上下文
        request.ctx.user = int(payload.get('sub'))
        
    except jwt.PyJWTError:
        request.ctx.user = None 