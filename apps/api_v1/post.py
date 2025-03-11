from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized

from models.post import Post, Post_Pydantic, PostIn_Pydantic
from models.tag import Tag
from schemas.post import PostCreate, PostUpdate, PostResponse

bp = Blueprint('posts_v1', url_prefix='/posts')


@bp.get('/')
async def get_posts(request):
    posts = await Post.all().prefetch_related('author', 'tags')
    post_data = [PostResponse.model_validate(post).model_dump(mode='json') for post in posts]
    return json(post_data)


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
    
    # 处理标签 - 使用tags而不是标签名称
    if post_data.tags:
        for tag_id in post_data.tags:
            tag = await Tag.get_or_none(id=tag_id)
            if tag:  # 只添加存在的标签
                await post.tags.add(tag)
    
    # 获取完整的文章数据
    await post.fetch_related('author', 'tags')
    post_data = PostResponse.model_validate(post)
    
    return json(post_data.model_dump(mode='json'))


@bp.get('/<post_id:int>')
async def get_post(request, post_id: int):
    post = await Post.get_or_none(id=post_id).prefetch_related('author', 'tags')
    if not post:
        raise NotFound("文章不存在")
    
    post_data = PostResponse.model_validate(post)
    return json(post_data.model_dump(mode='json'))


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
    update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})
    if update_data:
        await Post.filter(id=post_id).update(**update_data)
        post = await Post.get(id=post_id)
    
    # 处理标签 - 使用tags而不是标签名称
    if post_data.tags is not None:
        # 清除现有标签
        await post.tags.clear()
        
        # 添加新标签
        for tag_id in post_data.tags:
            tag = await Tag.get_or_none(id=tag_id)
            if tag:  # 只添加存在的标签
                await post.tags.add(tag)
    
    # 获取更新后的文章
    await post.fetch_related('author', 'tags')
    post_data = PostResponse.model_validate(post)
    
    return json(post_data.model_dump(mode='json'))


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