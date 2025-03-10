# Sanic 示例项目

这是一个基于 Sanic 的 RESTful API 示例项目，展示了如何使用 Sanic 框架构建一个功能完整的后端应用。

## 功能特性

- 使用 **Tortoise ORM** 进行数据库操作，支持一对多和多对多关系
- 使用 **Pydantic** 进行数据验证和序列化
- 实现 **JWT** 认证和自动刷新 token 功能
- 支持 **API 版本控制**（V1/V2）
- 采用模块化蓝图（Blueprint）组织代码结构

## 项目结构 
├── app.py # 主应用入口
├── config.py # 配置文件
├── models/ # Tortoise ORM 数据模型
│ ├── init.py
│ ├── user.py # 用户模型
│ ├── post.py # 文章模型（一对多关系）
│ └── tag.py # 标签模型（多对多关系）
├── schemas/ # Pydantic 模式
│ ├── init.py
│ ├── user.py
│ ├── post.py
│ └── token.py
├── apps/ # 路由分组
│ ├── init.py
│ ├── api_v1/ # API v1 版本
│ │ ├── init.py
│ │ ├── user.py
│ │ └── post.py
│ ├── api_v2/ # API v2 版本
│ │ ├── init.py
│ │ ├── user.py
│ │ └── post.py
│ └── auth/ # 认证模块
│ ├── init.py
│ └── routes.py
├── middlewares/ # 中间件
│ ├── init.py
│ └── auth.py # JWT验证中间件
└── services/ # 业务逻辑
├── init.py
└── auth.py # 认证服务
```

## 技术栈

- [Sanic](https://sanic.dev/) - 异步 Python Web 框架
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/) - 异步 ORM 框架
- [Pydantic](https://docs.pydantic.dev/) - 数据验证和序列化库
- [PyJWT](https://pyjwt.readthedocs.io/) - JWT 实现
- [Passlib](https://passlib.readthedocs.io/) - 密码哈希处理库

## 安装与启动

### 前置条件

- Python 3.8+
- pip

### 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install sanic tortoise-orm pydantic[email] passlib[bcrypt] pyjwt
```

### 启动应用

```bash
python app.py
```

默认情况下，应用将在 http://0.0.0.0:8000 运行。

## API 接口说明

### 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /auth/register | 用户注册 |
| POST | /auth/login | 用户登录 |
| POST | /auth/refresh | 刷新访问令牌 |

### 用户接口 (API v1)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/users/ | 获取所有用户 |
| GET | /api/v1/users/\<user_id\> | 获取特定用户 |
| GET | /api/v1/users/me | 获取当前用户信息 |
| PUT | /api/v1/users/me | 更新当前用户信息 |

### 文章接口 (API v1)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/posts/ | 获取所有文章 |
| POST | /api/v1/posts/ | 创建新文章 |
| GET | /api/v1/posts/\<post_id\> | 获取特定文章 |
| PUT | /api/v1/posts/\<post_id\> | 更新文章 |
| DELETE | /api/v1/posts/\<post_id\> | 删除文章 |

API v2 提供相同的端点，位于 `/api/v2/` 路径下。

## 数据模型关系

- **用户 (User)** 与 **文章 (Post)**: 一对多关系
- **文章 (Post)** 与 **标签 (Tag)**: 多对多关系

## 认证流程

1. 用户通过 `/auth/register` 注册或 `/auth/login` 登录
2. 认证成功后，服务器返回 `access_token` 和 `refresh_token`
3. 客户端在后续请求的 `Authorization` 头中包含 `Bearer <access_token>`
4. 当 `access_token` 过期时，使用 `/auth/refresh` 和 `refresh_token` 获取新的 `access_token`

## 开发与扩展

### 增加新 API 版本

1. 在 `apps/` 下创建新的版本目录（如 `api_v3/`）
2. 在 `app.py` 中注册新版本的蓝图

### 添加新实体模型

1. 在 `models/` 下创建新模型文件
2. 在 `config.py` 的 `MODELS` 列表中添加新模型
3. 在 `schemas/` 下创建对应的 Pydantic 模型
4. 在相应的 API 版本目录中创建路由处理文件

## 许可证

[MIT License](LICENSE)# sanic_demo_v2
