from sanic import Blueprint

# Create a blueprint for API v1
bp = Blueprint('api_v1')

# Import route modules
from . import users, posts, tags

# Group all API v1 blueprints under a common prefix
api_v1_group = Blueprint.group(users.bp, posts.bp, tags.bp, url_prefix='/api/v1') 