from sanic import Blueprint

# 创建 auth 主蓝图
bp = Blueprint('auth', url_prefix='/auth')

# 导入路由
from .routes import bp 