from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized
from sanic.request import Request

from middlewares.auth import protected

from services.tag_service import TagService
from schemas.tag import TagCreate, TagUpdate, TagResponse, TagWithPostCount
from core.pagination import PaginationParams
from core.di import inject

# Create a blueprint for tag-related endpoints
bp = Blueprint('tags_v1', url_prefix='/tags')

# Initialize services using dependency injection
tag_service = TagService()

@bp.get('/')
async def get_tags(request: Request):
    """
    Retrieve all tags.
    
    This endpoint returns a list of all tags in the system.
    Authentication is optional.
    
    Query parameters:
        - page: Page number (default: 1)
        - page_size: Items per page (default: 10, max: 100)
    
    Returns:
        JSON array of tag objects
    """
    # Get pagination parameters from query string
    page = int(request.args.get('page', 1))
    page_size = min(int(request.args.get('page_size', 10)), 100)
    pagination = PaginationParams(page=page, page_size=page_size)
    
    # Get tags using the service
    result = await tag_service.get_all_tags(pagination)
    
    return json(result.model_dump(mode='json'))


@bp.get('/<tag_id:int>')
async def get_tag(request: Request, tag_id: int):
    """
    Retrieve a specific tag by its ID with post count.
    
    Path parameters:
        - tag_id: The ID of the tag to retrieve
    
    Returns:
        JSON object containing the tag data with post count
        404 error if tag doesn't exist
    """
    # Get tag using the service
    tag = await tag_service.get_tag_with_post_count(tag_id)
    
    if not tag:
        raise NotFound("Tag not found")
    
    return json(tag)


@bp.get('/name/<name:str>')
async def get_tag_by_name(request: Request, name: str):
    """
    Retrieve a specific tag by its name.
    
    Path parameters:
        - name: The name of the tag to retrieve
    
    Returns:
        JSON object containing the tag data
        404 error if tag doesn't exist
    """
    # Get tag using the service
    tag = await tag_service.get_tag_by_name(name)
    
    if not tag:
        raise NotFound("Tag not found")
    
    # Convert to response format
    tag_response = TagResponse.model_validate(tag)
    return json(tag_response.model_dump(mode='json'))


@bp.post('/')
@protected()
async def create_tag(request: Request):
    """
    Create a new tag with the provided data.
    
    This endpoint creates a new tag.
    Authentication is required.
    
    Request body:
        - name: Tag name (required)
    
    Returns:
        JSON object containing the created tag data
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Validate request data using Pydantic model
    tag_data = TagCreate(**request.json)
    
    # Create tag using the service
    tag = await tag_service.create_tag(tag_data)
    
    # Convert to response format
    tag_response = TagResponse.model_validate(tag)
    return json(tag_response.model_dump(mode='json'))


@bp.put('/<tag_id:int>')
@protected()
async def update_tag(request: Request, tag_id: int):
    """
    Update an existing tag.
    
    This endpoint updates a tag.
    Authentication is required.
    
    Path parameters:
        - tag_id: The ID of the tag to update
    
    Request body:
        - name: Updated tag name (required)
    
    Returns:
        JSON object containing the updated tag data
        404 error if tag doesn't exist
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Validate request data
    tag_data = TagUpdate(**request.json)
    
    # Update tag using the service
    updated_tag = await tag_service.update_tag(tag_id, tag_data)
    
    if not updated_tag:
        raise NotFound("Tag not found")
    
    # Convert to response format
    tag_response = TagResponse.model_validate(updated_tag)
    return json(tag_response.model_dump(mode='json'))


@bp.delete('/<tag_id:int>')
@protected()
async def delete_tag(request: Request, tag_id: int):
    """
    Delete a specific tag.
    
    This endpoint deletes a tag.
    Authentication is required.
    
    Path parameters:
        - tag_id: The ID of the tag to delete
    
    Returns:
        JSON confirmation message
        404 error if tag doesn't exist
    """
    # Verify user is authenticated
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("Please login first")
    
    # Delete tag using the service
    success = await tag_service.delete_tag(tag_id)
    
    if not success:
        raise NotFound("Tag not found")
    
    return json({"message": "Tag deleted successfully"})


@bp.get('/<tag_id:int>/posts')
async def get_tag_posts(request: Request, tag_id: int):
    """
    Retrieve all posts with a specific tag.
    
    Path parameters:
        - tag_id: The ID of the tag
    
    Query parameters:
        - page: Page number (default: 1)
        - page_size: Items per page (default: 10, max: 100)
    
    Returns:
        JSON object containing the tag and its associated posts
        404 error if tag doesn't exist
    """
    # Get pagination parameters from query string
    page = int(request.args.get('page', 1))
    page_size = min(int(request.args.get('page_size', 10)), 100)
    pagination = PaginationParams(page=page, page_size=page_size)
    
    # Get tag posts using the service
    result = await tag_service.get_tag_posts(tag_id, pagination)
    
    if not result:
        raise NotFound("Tag not found")
    
    return json(result) 