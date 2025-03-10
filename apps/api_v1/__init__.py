from sanic import Blueprint

# 创建API版本蓝图
bp = Blueprint('api_v1')

# 导入子模块
from . import user, post, tag

# 使用 group 方法组合子蓝图
api_v1_group = Blueprint.group(user.bp, post.bp, tag.bp, url_prefix='/api/v1') 