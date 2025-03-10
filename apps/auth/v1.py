from sanic import Blueprint, json
from sanic.exceptions import Unauthorized

from models.user import User
from schemas.user import UserCreate
from schemas.token import Token
from services.auth import (
    get_password_hash, authenticate_user,
    create_access_token, create_refresh_token, decode_token
)

# 创建版本特定的蓝图，但没有前缀
# URL前缀将由上层蓝图和应用层提供
bp = Blueprint('auth_v1')

@bp.post('/register')
async def register(request):
    data = request.json
    user_data = UserCreate(**data)
    
    # 检查用户是否已存在
    existing_user = await User.filter(username=user_data.username).first() or await User.filter(email=user_data.email).first()
    if existing_user:
        return json({"error": "用户名或邮箱已存在"}, status=400)
    
    # 创建新用户
    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password)
    )
    
    # 生成令牌
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return json({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})


@bp.post('/login')
async def login(request):
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return json({"error": "请提供用户名和密码"}, status=400)
    
    user = await authenticate_user(username, password)
    if not user:
        return json({"error": "用户名或密码错误"}, status=401)
    
    # 生成令牌
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return json({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})


@bp.post('/refresh')
async def refresh_token(request):
    data = request.json
    refresh_token = data.get("refresh_token")
    
    if not refresh_token:
        return json({"error": "请提供刷新令牌"}, status=400)
    
    payload = decode_token(refresh_token)
    if not payload or "refresh" not in payload:
        return json({"error": "无效的刷新令牌"}, status=401)
    
    user_id = int(payload.get("sub"))
    
    # 生成新的访问令牌
    new_access_token = create_access_token(user_id)
    
    return json({"access_token": new_access_token, "token_type": "bearer"}) 