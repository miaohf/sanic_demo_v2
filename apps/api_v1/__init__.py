from sanic import Blueprint

from .posts import bp as posts_bp
from .tags import bp as tags_bp
from .users import bp as users_bp

# Create a parent blueprint for API v1
api_v1 = Blueprint.group(posts_bp, tags_bp, users_bp, url_prefix='/api/v1') 