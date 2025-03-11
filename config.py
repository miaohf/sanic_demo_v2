import os
from datetime import timedelta

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