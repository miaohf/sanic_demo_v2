from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized

from models.post import Post, Post_Pydantic, PostIn_Pydantic
from models.tag import Tag
from schemas.post import PostCreate, PostUpdate, PostResponse

# Create a blueprint for post-related endpoints with URL prefix '/posts'
bp = Blueprint('posts_v1', url_prefix='/posts')


@bp.get('/')
async def get_posts(request):
    """
    Retrieve all posts with their related authors and tags.
    
    This endpoint returns a list of all posts in the system.
    Authentication is required.
    
    Returns:
        JSON array of post objects with author and tag information
    """
    # Fetch all posts and load related author and tag data
    posts = await Post.all().prefetch_related('author', 'tags')
    post_data = [PostResponse.model_validate(post).model_dump(mode='json') for post in posts]
    return json(post_data)


@bp.post('/')
async def create_post(request):
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
    data = request.json
    post_data = PostCreate(**data)
    
    # Create the post in database
    post = await Post.create(
        title=post_data.title,
        content=post_data.content,
        author_id=user_id
    )
    
    # Process tags if provided
    if post_data.tags:
        # Get valid tags that match the provided IDs
        valid_tags = await Tag.filter(id__in=post_data.tags)
        # Associate tags with the post in a single operation
        await post.tags.add(*valid_tags)
    
    # Load related data for the response
    await post.fetch_related('author', 'tags')
    post_data = PostResponse.model_validate(post)
    
    return json(post_data.model_dump(mode='json'))


@bp.get('/<post_id:int>')
async def get_post(request, post_id: int):
    """
    Retrieve a specific post by its ID.
    
    Path parameters:
        - post_id: The ID of the post to retrieve
    
    Returns:
        JSON object containing the post data
        404 error if post doesn't exist
    """
    # Find post by ID with related author and tags
    post = await Post.get_or_none(id=post_id).prefetch_related('author', 'tags')
    if not post:
        raise NotFound("Post not found")
    
    # Convert to response format
    post_data = PostResponse.model_validate(post)
    return json(post_data.model_dump(mode='json'))


@bp.put('/<post_id:int>')
async def update_post(request, post_id: int):
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
    
    # Find post and verify ownership
    post = await Post.get_or_none(id=post_id, author_id=user_id)
    if not post:
        raise NotFound("Post not found or you don't have permission to modify it")
    
    # Validate request data
    data = request.json
    post_data = PostUpdate(**data)
    
    # Update post fields excluding tags (handled separately)
    update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})
    if update_data:
        await Post.filter(id=post_id).update(**update_data)
        post = await Post.get(id=post_id)
    
    # Update tags if provided in request
    if post_data.tags is not None:
        # Remove all existing tag associations
        await post.tags.clear()
        
        # Add new tag associations
        for tag_id in post_data.tags:
            tag = await Tag.get_or_none(id=tag_id)
            if tag:  # Only add if tag exists
                await post.tags.add(tag)
    
    # Load related data for the response
    await post.fetch_related('author', 'tags')
    post_data = PostResponse.model_validate(post)
    
    return json(post_data.model_dump(mode='json'))


@bp.delete('/<post_id:int>')
async def delete_post(request, post_id: int):
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
    
    # Find post and verify ownership
    post = await Post.get_or_none(id=post_id, author_id=user_id)
    if not post:
        raise NotFound("Post not found or you don't have permission to delete it")
    
    # Delete the post
    await post.delete()
    return json({"message": "Post deleted successfully"}) 