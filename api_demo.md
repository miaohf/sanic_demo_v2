# API 测试示例 (curl)

这里提供了使用 curl 命令测试 API 的示例。使用前请确保应用已经启动。

## 认证 API

### 1. 用户注册

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. 用户登录

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

输出示例：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. 刷新令牌

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

## 用户 API (API v1)

以下命令需要使用从登录接口获取的 access_token。

### 1. 获取所有用户

```bash
curl -X GET http://localhost:8000/api/v1/users/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. 获取特定用户

```bash
curl -X GET http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. 获取当前用户信息

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. 更新当前用户信息

```bash
curl -X PUT http://localhost:8000/api/v1/users/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "username": "updated_username",
    "email": "updated@example.com"
  }'
```

## 文章 API (API v1)

### 1. 获取所有文章

```bash
curl -X GET http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. 创建新文章

```bash
curl -X POST http://localhost:8000/api/v1/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "测试文章标题",
    "content": "这是一篇测试文章的内容",
    "tags": ["技术", "Python", "Sanic"]
  }'
```

### 3. 获取特定文章

```bash
curl -X GET http://localhost:8000/api/v1/posts/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. 更新文章

```bash
curl -X PUT http://localhost:8000/api/v1/posts/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "更新后的文章标题",
    "content": "这是更新后的文章内容",
    "tags": ["更新", "技术博客"]
  }'
```

### 5. 删除文章

```bash
curl -X DELETE http://localhost:8000/api/v1/posts/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## API v2 测试

将以上命令中的路径从 `/api/v1/` 改为 `/api/v2/` 即可测试 v2 版本的 API。例如：

```bash
curl -X GET http://localhost:8000/api/v2/users/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 响应示例

### 用户登录成功响应

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 获取用户信息响应

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "created_at": "2023-05-01T12:34:56.789Z",
  "updated_at": "2023-05-01T12:34:56.789Z"
}
```

### 获取文章响应

```json
{
  "id": 1,
  "title": "测试文章标题",
  "content": "这是一篇测试文章的内容",
  "created_at": "2023-05-01T12:34:56.789Z",
  "updated_at": "2023-05-01T12:34:56.789Z",
  "author_id": 1,
  "tags": [
    {
      "id": 1,
      "name": "技术"
    },
    {
      "id": 2,
      "name": "Python"
    },
    {
      "id": 3,
      "name": "Sanic"
    }
  ]
}
```

## 标签 API (API v1)

以下命令需要使用从登录接口获取的 access_token。

### 1. 获取所有标签

```bash
curl -X GET http://localhost:8000/api/v1/tags/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. 获取特定标签

```bash
curl -X GET http://localhost:8000/api/v1/tags/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. 通过名称获取标签

```bash
curl -X GET http://localhost:8000/api/v1/tags/name/技术 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. 创建新标签

```bash
curl -X POST http://localhost:8000/api/v1/tags/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "name": "新标签"
  }'
```

### 5. 更新标签

```bash
curl -X PUT http://localhost:8000/api/v1/tags/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "name": "更新后的标签名称"
  }'
```

### 6. 删除标签

```bash
curl -X DELETE http://localhost:8000/api/v1/tags/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 7. 获取标签关联的文章

```bash
curl -X GET http://localhost:8000/api/v1/tags/1/posts \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 响应示例

### 获取标签列表响应

```json
[
  {
    "id": 1,
    "name": "技术"
  },
  {
    "id": 2,
    "name": "Python"
  },
  {
    "id": 3,
    "name": "Sanic"
  }
]
```

### 获取单个标签响应

```json
{
  "id": 1,
  "name": "技术"
}
```

### 获取标签关联文章响应

```json
{
  "tag": {
    "id": 1,
    "name": "技术"
  },
  "posts": [
    {
      "id": 1,
      "title": "测试文章标题",
      "content": "这是一篇测试文章的内容",
      "created_at": "2023-05-01T12:34:56.789Z",
      "updated_at": "2023-05-01T12:34:56.789Z",
      "author_id": 1,
      "tags": [
        {
          "id": 1,
          "name": "技术"
        },
        {
          "id": 2,
          "name": "Python"
        }
      ]
    }
  ]
}
```
```

您可以将此内容保存为项目中的 `api_demo.md` 文件，作为 API 测试的参考文档。 