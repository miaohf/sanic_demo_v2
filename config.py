import os
from datetime import timedelta
from typing import Dict, Any
from pydantic import BaseModel

# Basic application configuration
DEBUG = True  # Enable debug mode for development
APP_NAME = "SanicDemo"  # Application name used by Sanic
HOST = "0.0.0.0"  # Host address to bind the server to
PORT = 8000  # Port number to listen on

# Database configuration
DB_URL = os.getenv("DB_URL", "sqlite://db.sqlite3")  # Database connection URL with fallback
MODELS = ["models.user", "models.post", "models.tag"]  # List of model modules to register

# JWT authentication configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")  # Secret key for JWT encoding/decoding
JWT_ALGORITHM = "HS256"  # Algorithm used for JWT encoding
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access token expiration time
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token expiration time

class Settings(BaseModel):
    """Application settings"""
    # App settings
    APP_NAME: str = "blog_api"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str = f"sqlite:///{os.path.abspath('blog.db')}"
    
    # JWT settings
    JWT_SECRET: str = "your-secret-key"  # 在生产环境中应该使用环境变量
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    def dict(self) -> dict:
        """兼容方法，返回设置字典"""
        return self.model_dump()
    
    @classmethod
    def from_env(cls):
        """从环境变量创建设置"""
        return cls(
            APP_NAME=os.getenv("APP_NAME", "blog_api"),
            DEBUG=os.getenv("DEBUG", "True").lower() in ("true", "1", "t"),
            HOST=os.getenv("HOST", "0.0.0.0"),
            PORT=int(os.getenv("PORT", "8000")),
            DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///blog.db"),
            JWT_SECRET=os.getenv("JWT_SECRET", "your-secret-key"),
            JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256"),
            JWT_ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            JWT_REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7")),
            CORS_ORIGINS=os.getenv("CORS_ORIGINS", "*").split(",")
        )

# 创建设置实例（可以选择从环境变量加载）
# settings = Settings.from_env()  # 从环境变量加载
settings = Settings()  # 使用默认值 