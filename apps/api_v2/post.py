from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized

from models.post import Post, Post_Pydantic, PostIn_Pydantic
from models.tag import Tag
from schemas.post import PostCreate, PostUpdate

bp = Blueprint('posts_v2', url_prefix='/posts')


@bp.get('/')
async def get_posts(request):
    posts = await Post.all().prefetch_related('author', 'tags')
    post_data = await Post_Pydantic.from_queryset(Post.all())
    return json([post.dict() for post in post_data])


@bp.post('/')
async def create_post(request):
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    data = request.json
    post_data = PostCreate(**data)
    
    # 创建文章
    post = await Post.create(
        title=post_data.title,
        content=post_data.content,
        author_id=user_id
    )
    
    # 处理标签
    if post_data.tags:
        for tag_name in post_data.tags:
            tag, _ = await Tag.get_or_create(name=tag_name)
            await post.tags.add(tag)
    
    # 获取完整的文章数据
    await post.fetch_related('author', 'tags')
    post_data = await Post_Pydantic.from_tortoise_orm(post)
    
    return json(post_data.dict())


@bp.get('/<post_id:int>')
async def get_post(request, post_id: int):
    post = await Post.get_or_none(id=post_id).prefetch_related('author', 'tags')
    if not post:
        raise NotFound("文章不存在")
    
    post_data = await Post_Pydantic.from_tortoise_orm(post)
    return json(post_data.dict())


@bp.put('/<post_id:int>')
async def update_post(request, post_id: int):
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    post = await Post.get_or_none(id=post_id, author_id=user_id)
    if not post:
        raise NotFound("文章不存在或您无权修改")
    
    data = request.json
    post_data = PostUpdate(**data)
    
    # 更新文章信息
    update_data = post_data.dict(exclude_unset=True, exclude={"tags"})
    if update_data:
        await Post.filter(id=post_id).update(**update_data)
        post = await Post.get(id=post_id)
    
    # 处理标签
    if post_data.tags is not None:
        # 清除现有标签
        await post.tags.clear()
        
        # 添加新标签
        for tag_name in post_data.tags:
            tag, _ = await Tag.get_or_create(name=tag_name)
            await post.tags.add(tag)
    
    # 获取更新后的文章
    await post.fetch_related('author', 'tags')
    post_data = await Post_Pydantic.from_tortoise_orm(post)
    
    return json(post_data.dict())


@bp.delete('/<post_id:int>')
async def delete_post(request, post_id: int):
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    post = await Post.get_or_none(id=post_id, author_id=user_id)
    if not post:
        raise NotFound("文章不存在或您无权删除")
    
    await post.delete()
    return json({"message": "文章已删除"}) 