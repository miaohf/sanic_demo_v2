from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized

from models.tag import Tag
from models.post import Post
from schemas.tag import TagResponse, TagBase, TagCreate, TagUpdate, TagWithPostCount
from schemas.post import PostResponse

# Create a blueprint for tag-related endpoints
bp = Blueprint('tags_v2', url_prefix='/tags')

@bp.get('/')
async def get_tags(request):
    """
    Retrieve all tags.
    
    This endpoint returns a list of all tags in the system.
    
    Returns:
        JSON array of tag objects
    """
    tags = await Tag.all()
    tag_data = [TagResponse.model_validate(tag).model_dump(mode='json') for tag in tags]
    return json(tag_data)

@bp.get('/<tag_id:int>')
async def get_tag(request, tag_id: int):
    """
    Retrieve a specific tag by ID.
    
    Path parameters:
        - tag_id: The ID of the tag to retrieve
    
    Returns:
        JSON object containing the tag data
        404 error if tag doesn't exist
    """
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    tag_data = TagResponse.model_validate(tag)
    return json(tag_data.model_dump(mode='json'))

@bp.post('/')
async def create_tag(request):
    """
    Create a new tag.
    
    This endpoint creates a new tag.
    Authentication is required.
    
    Request body:
        - name: Tag name (required)
    
    Returns:
        JSON object containing the created tag data
        400 error if tag already exists
    """
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    data = request.json
    tag_data = TagBase(**data)
    
    # Check if tag already exists
    existing_tag = await Tag.filter(name=tag_data.name).first()
    if existing_tag:
        return json({
            "message": "标签已存在", 
            "tag": TagResponse.model_validate(existing_tag).model_dump(mode='json')
        })
    
    # Create new tag
    tag = await Tag.create(name=tag_data.name)
    tag_data = TagResponse.model_validate(tag)
    
    return json(tag_data.model_dump(mode='json'))

@bp.put('/<tag_id:int>')
async def update_tag(request, tag_id: int):
    """
    Update an existing tag.
    
    This endpoint updates a tag's information.
    Authentication is required.
    
    Path parameters:
        - tag_id: The ID of the tag to update
    
    Request body:
        - name: Updated tag name (required)
    
    Returns:
        JSON object containing the updated tag data
        404 error if tag doesn't exist
    """
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    data = request.json
    tag_data = TagBase(**data)
    
    # Check if new name already exists
    if tag.name != tag_data.name:
        existing_tag = await Tag.filter(name=tag_data.name).first()
        if existing_tag:
            return json({"error": "标签名称已被使用"}, status=400)
    
    # Update tag
    tag.name = tag_data.name
    await tag.save()
    
    # Return updated tag
    tag_data = TagResponse.model_validate(tag)
    return json(tag_data.model_dump(mode='json'))

@bp.delete('/<tag_id:int>')
async def delete_tag(request, tag_id: int):
    """
    Delete a tag.
    
    This endpoint deletes an existing tag.
    Authentication is required.
    
    Path parameters:
        - tag_id: The ID of the tag to delete
    
    Returns:
        JSON confirmation message
        404 error if tag doesn't exist
    """
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    # Get count of associated posts
    post_count = await tag.posts.all().count()
    
    # Delete tag
    await tag.delete()
    
    return json({
        "message": "标签已删除",
        "affected_posts": post_count
    })

@bp.get('/<tag_id:int>/posts')
async def get_tag_posts(request, tag_id: int):
    """
    Retrieve all posts associated with a specific tag.
    
    Path parameters:
        - tag_id: The ID of the tag to retrieve posts for
    
    Returns:
        JSON object containing the tag and its associated posts
        404 error if tag doesn't exist
    """
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    # Get posts with this tag
    posts = await tag.posts.all().prefetch_related('author', 'tags')
    
    # Serialize post data
    post_data = [PostResponse.model_validate(post).model_dump(mode='json') for post in posts]
    
    return json({
        "tag": TagResponse.model_validate(tag).model_dump(mode='json'),
        "posts": post_data
    })

@bp.get('/name/<tag_name:str>')
async def get_tag_by_name(request, tag_name: str):
    """
    Retrieve a specific tag by name.
    
    Path parameters:
        - tag_name: The name of the tag to retrieve
    
    Returns:
        JSON object containing the tag data
        404 error if tag doesn't exist
    """
    tag = await Tag.get_or_none(name=tag_name)
    if not tag:
        raise NotFound("标签不存在")
    
    tag_data = TagResponse.model_validate(tag)
    return json(tag_data.model_dump(mode='json')) 