# API V2 包 
from sanic import Blueprint

# 创建API版本蓝图
bp = Blueprint('api_v2')

# 导入子模块
from . import users, posts, tags

# 使用 group 方法组合子蓝图
api_v2_group = Blueprint.group(users.bp, posts.bp, tags.bp, url_prefix='/api/v2') 