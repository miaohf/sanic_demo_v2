from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized
from sanic.request import Request

from services.post_service import PostService
from repositories.post_repository import PostRepository
from repositories.tag_repository import TagRepository
from schemas.post import PostCreate, PostUpdate, PostResponse
from core.pagination import PaginationParams
from core.di import inject

# Create a blueprint for post-related endpoints
bp = Blueprint('posts_v1', url_prefix='/posts')

# Initialize services using dependency injection
post_service = PostService()

@bp.get('/')
async def get_posts(request: Request):
    """
    Retrieve all posts with their related authors and tags.
    
    This endpoint returns a list of all posts in the system.
    Authentication is optional.
    
    Query parameters:
        - page: Page number (default: 1)
        - page_size: Items per page (default: 10, max: 100)
    
    Returns:
        JSON array of post objects with author and tag information
    """
    # Get pagination parameters from query string
    page = int(request.args.get('page', 1))
    page_size = min(int(request.args.get('page_size', 10)), 100)
    pagination = PaginationParams(page=page, page_size=page_size)
    
    # Get posts using the service
    result = await post_service.get_all_posts(pagination)
    
    return json(result.model_dump(mode='json'))


@bp.post('/')
async def create_post(request: Request):
    """
    Create a new post with the provided data.
    
    This endpoint creates a new post owned by the authenticated user.
    Authentication is required.
    
    Request body:
        - title: Post title (required)
        - content: Post content (required)
        - tags: List of tag IDs to associate with the post (optional)
    
    Returns:
        JSON object containing the created post data
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Validate request data using Pydantic model
    post_data = PostCreate(**request.json)
    
    # Create post using the service
    post = await post_service.create_post(user_id, post_data)
    
    # Convert to response format
    post_response = PostResponse.model_validate(post)
    return json(post_response.model_dump(mode='json'))


@bp.get('/<post_id:int>')
async def get_post(request: Request, post_id: int):
    """
    Retrieve a specific post by its ID.
    
    Path parameters:
        - post_id: The ID of the post to retrieve
    
    Returns:
        JSON object containing the post data
        404 error if post doesn't exist
    """
    # Get post using the service
    post = await post_service.get_post(post_id)
    
    if not post:
        raise NotFound("Post not found")
    
    # Convert to response format
    post_response = PostResponse.model_validate(post)
    return json(post_response.model_dump(mode='json'))


@bp.put('/<post_id:int>')
async def update_post(request: Request, post_id: int):
    """
    Update an existing post.
    
    This endpoint updates a post owned by the authenticated user.
    Authentication is required.
    
    Path parameters:
        - post_id: The ID of the post to update
    
    Request body:
        - title: Updated post title (optional)
        - content: Updated post content (optional)
        - tags: Updated list of tag IDs (optional)
    
    Returns:
        JSON object containing the updated post data
        404 error if post doesn't exist or user doesn't own it
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Validate request data
    post_data = PostUpdate(**request.json)
    
    # Update post using the service
    updated_post = await post_service.update_post(post_id, user_id, post_data)
    
    if not updated_post:
        raise NotFound("Post not found or you don't have permission to modify it")
    
    # Convert to response format
    post_response = PostResponse.model_validate(updated_post)
    return json(post_response.model_dump(mode='json'))


@bp.delete('/<post_id:int>')
async def delete_post(request: Request, post_id: int):
    """
    Delete a specific post.
    
    This endpoint deletes a post owned by the authenticated user.
    Authentication is required.
    
    Path parameters:
        - post_id: The ID of the post to delete
    
    Returns:
        JSON confirmation message
        404 error if post doesn't exist or user doesn't own it
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Delete post using the service
    success = await post_service.delete_post(post_id, user_id)
    
    if not success:
        raise NotFound("Post not found or you don't have permission to delete it")
    
    return json({"message": "Post deleted successfully"}) 