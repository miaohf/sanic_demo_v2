from sanic import Sanic
from sanic.response import json
from tortoise.contrib.sanic import register_tortoise
from sanic_cors import CORS

from config import settings
from middlewares.auth import jwt_middleware
from apps.auth.routes import bp as auth_bp
from apps.api_v1 import api_v1
# from apps.api_v2 import api_v2

from core.di import container
from core.logging import Logger, app_logger
from core.events import EventBus, EventType, event_bus

from repositories.post_repository import PostRepository
from repositories.tag_repository import TagRepository
from repositories.user_repository import UserRepository

from services.post_service import PostService
from services.tag_service import TagService
from services.user_service import UserService

def create_app():
    """创建 Sanic 应用"""
    app = Sanic("blog_api")
    app.config.update(settings.dict())
    
    # 注册 CORS 中间件
    CORS(app)
    
    # 注册中间件
    app.register_middleware(jwt_middleware, "request")
    
    # 配置 Tortoise ORM - 确保这个在蓝图注册之前执行
    register_tortoise(
        app,
        db_url=app.config.DATABASE_URL,
        modules={"models": ["models"]},  # 确保这里包含您所有的模型模块
        generate_schemas=True
    )
    
    # 初始化依赖注入和服务
    _initialize_services()
    
    # 注册事件处理程序
    _register_event_handlers()
    
    # 注册蓝图 - 在 Tortoise 初始化之后
    app.blueprint(auth_bp)
    app.blueprint(api_v1)
    # app.blueprint(api_v2)
    
    @app.route("/")
    async def index(request):
        return json({"message": "Welcome to the Blog API"})
    
    return app

def _initialize_services():
    """初始化服务和依赖注入"""
    # 创建仓库实例
    post_repo = PostRepository()
    tag_repo = TagRepository()
    user_repo = UserRepository()
    
    # 注册到依赖注入容器
    container.register(PostRepository, post_repo)
    container.register(TagRepository, tag_repo)
    container.register(UserRepository, user_repo)
    container.register(Logger, app_logger)
    container.register(EventBus, event_bus)
    
    # 创建服务实例
    post_service = PostService(
        post_repository=post_repo,
        tag_repository=tag_repo,
        user_repository=user_repo,
        logger=app_logger,
        event_bus=event_bus
    )
    
    tag_service = TagService(
        tag_repository=tag_repo,
        logger=app_logger,
        event_bus=event_bus
    )
    
    user_service = UserService(
        user_repository=user_repo,
        logger=app_logger,
        event_bus=event_bus
    )
    
    # 注册服务到容器
    container.register(PostService, post_service)
    container.register(TagService, tag_service)
    container.register(UserService, user_service)

def _register_event_handlers():
    """注册事件处理程序"""
    @event_bus.subscribe(EventType.POST_CREATED)
    async def handle_post_created(post_id):
        """处理文章创建事件"""
        app_logger.info(f"Post created event: {post_id}")
    
    @event_bus.subscribe(EventType.POST_UPDATED)
    async def handle_post_updated(post_id):
        """处理文章更新事件"""
        app_logger.info(f"Post updated event: {post_id}")
    
    @event_bus.subscribe(EventType.POST_DELETED)
    async def handle_post_deleted(post_id):
        """处理文章删除事件"""
        app_logger.info(f"Post deleted event: {post_id}")

app = create_app()

if __name__ == "__main__":
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG
    )