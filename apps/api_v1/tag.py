from sanic import Blueprint, json
from sanic.exceptions import NotFound, Unauthorized

from models.tag import Tag
from models.post import Post
from schemas.post import TagResponse, TagBase

bp = Blueprint('tags_v1', url_prefix='/tags')

@bp.get('/')
async def get_tags(request):
    """获取所有标签"""
    tags = await Tag.all()
    tag_data = [TagResponse.model_validate(tag).model_dump(mode='json') for tag in tags]
    return json(tag_data)

@bp.get('/<tag_id:int>')
async def get_tag(request, tag_id: int):
    """获取特定标签"""
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    tag_data = TagResponse.model_validate(tag)
    return json(tag_data.model_dump(mode='json'))

@bp.post('/')
async def create_tag(request):
    """创建新标签"""
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    data = request.json
    tag_data = TagBase(**data)
    
    # 检查标签是否已存在
    existing_tag = await Tag.filter(name=tag_data.name).first()
    if existing_tag:
        return json({"message": "标签已存在", "tag": TagResponse.model_validate(existing_tag).model_dump(mode='json')})
    
    # 创建新标签
    tag = await Tag.create(name=tag_data.name)
    tag_data = TagResponse.model_validate(tag)
    
    return json(tag_data.model_dump(mode='json'))

@bp.put('/<tag_id:int>')
async def update_tag(request, tag_id: int):
    """更新标签"""
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    data = request.json
    tag_data = TagBase(**data)
    
    # 检查新名称是否已存在
    if tag.name != tag_data.name:
        existing_tag = await Tag.filter(name=tag_data.name).first()
        if existing_tag:
            return json({"error": "标签名称已被使用"}, status=400)
    
    # 更新标签
    tag.name = tag_data.name
    await tag.save()
    
    # 返回更新后的标签
    tag_data = TagResponse.model_validate(tag)
    return json(tag_data.model_dump(mode='json'))

@bp.delete('/<tag_id:int>')
async def delete_tag(request, tag_id: int):
    """删除标签"""
    user_id = request.ctx.user
    if not user_id:
        raise Unauthorized("请先登录")
    
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    # 获取关联的文章数量
    post_count = await tag.posts.all().count()
    
    # 删除标签
    await tag.delete()
    
    return json({
        "message": "标签已删除",
        "affected_posts": post_count
    })

@bp.get('/<tag_id:int>/posts')
async def get_tag_posts(request, tag_id: int):
    """获取标签关联的文章"""
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise NotFound("标签不存在")
    
    # 获取包含该标签的文章
    posts = await tag.posts.all().prefetch_related('author', 'tags')
    
    # 序列化文章数据
    from schemas.post import PostResponse
    post_data = [PostResponse.model_validate(post).model_dump(mode='json') for post in posts]
    
    return json({
        "tag": TagResponse.model_validate(tag).model_dump(mode='json'),
        "posts": post_data
    })

@bp.get('/name/<tag_name:str>')
async def get_tag_by_name(request, tag_name: str):
    """通过名称获取标签"""
    tag = await Tag.get_or_none(name=tag_name)
    if not tag:
        raise NotFound("标签不存在")
    
    tag_data = TagResponse.model_validate(tag)
    return json(tag_data.model_dump(mode='json')) 