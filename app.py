from sanic import Sanic
from sanic.response import json
from tortoise.contrib.sanic import register_tortoise

from config import DEBUG, APP_NAME, HOST, PORT, DB_URL, MODELS
from middlewares.auth import jwt_middleware
from apps.api_v1 import api_v1_group
from apps.api_v2 import api_v2_group
from apps.auth.routes import bp as auth_bp

# Initialize the Sanic application with the name from config
app = Sanic(APP_NAME)

# Register the JWT authentication middleware
# This middleware will process JWT tokens for every request
app.middleware("request")(jwt_middleware)

# Register API version blueprints
# These blueprints contain route handlers for different API versions
app.blueprint(api_v1_group)  # Register API v1 endpoints
app.blueprint(api_v2_group)  # Register API v2 endpoints

# Register authentication blueprint at the root level
# Auth endpoints are independent of API versions
app.blueprint(auth_bp)

# Configure Tortoise ORM
# This connects the application to the database and registers models
register_tortoise(
    app,
    db_url=DB_URL,  # Database connection string
    modules={"models": MODELS},  # Model modules to register
    generate_schemas=True  # Automatically create database tables
)

# Root endpoint that returns a welcome message
@app.route("/")
async def index(request):
    """
    Root endpoint that displays a welcome message.
    This is a public endpoint that doesn't require authentication.
    
    Returns:
        JSON response with a welcome message
    """
    return json({"message": "Welcome to Sanic API"})

# Run the application when executed directly
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)