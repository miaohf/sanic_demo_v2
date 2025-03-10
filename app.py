from sanic import Sanic
from sanic.response import json
from tortoise.contrib.sanic import register_tortoise

from config import DEBUG, APP_NAME, HOST, PORT, DB_URL, MODELS
from middlewares.auth import jwt_middleware
from apps.api_v1 import api_v1_group
from apps.api_v2 import api_v2_group
from apps.auth.routes import bp as auth_bp

app = Sanic(APP_NAME)

# 注册中间件
app.middleware("request")(jwt_middleware)

# 注册API版本蓝图
app.blueprint(api_v1_group)
app.blueprint(api_v2_group)

# 直接在根路径注册auth蓝图
app.blueprint(auth_bp)

# 设置Tortoise ORM
register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": MODELS},
    generate_schemas=True
)

@app.route("/")
async def index(request):
    return json({"message": "欢迎使用Sanic API"})

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)