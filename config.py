import os
from datetime import timedelta

# 基础配置
DEBUG = True
APP_NAME = "SanicDemo"
HOST = "0.0.0.0"
PORT = 8000

# 数据库配置
DB_URL = os.getenv("DB_URL", "sqlite://db.sqlite3")
MODELS = ["models.user", "models.post", "models.tag"]

# JWT配置
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30) 