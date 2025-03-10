from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized

from models.user import User
from schemas.user import UserUpdate, UserResponse

# 为 v1 版本的用户蓝图添加前缀
bp = Blueprint('users_v1', url_prefix='/users')


@bp.get('/')
async def get_users(request):
    users = await User.all()
    user_data = [UserResponse.model_validate(user).model_dump(mode='json') for user in users]
    return json(user_data)


@bp.get('/<user_id:int>')
async def get_user(request, user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise NotFound("用户不存在")
    
    user_data = UserResponse.model_validate(user)
    return json(user_data.model_dump(mode='json'))


@bp.put('/me')
async def update_user(request):
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    user = await User.get_or_none(id=user_id)
    if not user:
        raise NotFound("用户不存在")
    
    data = request.json
    user_data = UserUpdate(**data)
    
    # 更新用户信息
    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data:
        from services.auth import get_password_hash
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    await User.filter(id=user_id).update(**update_data)
    
    # 获取更新后的用户
    user = await User.get(id=user_id)
    user_data = UserResponse.model_validate(user)
    
    return json(user_data.model_dump(mode='json'))


@bp.get('/me')
async def get_my_info(request):
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    user = await User.get_or_none(id=user_id)
    if not user:
        raise NotFound("用户不存在")
    
    user_data = UserResponse.model_validate(user)
    return json(user_data.model_dump(mode='json')) 