# API Testing Examples (curl)

This document provides examples of testing the API using curl commands. Please ensure the application is running before using these examples.

## Authentication API

### 1. User Registration

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "email": "test@example.com",
    "password": "12345678"
  }'
```

### 2. User Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "12345678"
  }'
```

Example output:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Refresh Token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

## User API (API v1)

The following commands require the access_token obtained from the login endpoint.

### 1. Get All Users

```bash
curl -X GET http://localhost:8000/api/v1/users/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. Get Specific User

```bash
curl -X GET http://localhost:8000/api/v1/users/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. Get Current User Info

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Update Current User Info

```bash
curl -X PUT http://localhost:8000/api/v1/users/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "username": "updated_username",
    "email": "updated@example.com"
  }'
```

## Post API (API v1)

### 1. Get All Posts

```bash
curl -X GET http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. Create New Post

```bash
curl -X POST http://localhost:8000/api/v1/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Test Post Title",
    "content": "This is the content of a test post",
    "tags": [1, 2, 3]
  }'
```

### 3. Get Specific Post

```bash
curl -X GET http://localhost:8000/api/v1/posts/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Update Post

```bash
curl -X PUT http://localhost:8000/api/v1/posts/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Updated Post Title",
    "content": "This is the updated content of the post",
    "tags": ["Updated", "Tech Blog"]
  }'
```

### 5. Delete Post

```bash
curl -X DELETE http://localhost:8000/api/v1/posts/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## API v2 Testing

To test v2 version of the API, simply change the path from `/api/v1/` to `/api/v2/` in the above commands. For example:

```bash
curl -X GET http://localhost:8000/api/v2/users/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Response Examples

### Successful Login Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get User Info Response

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

### Get Post Response

```json
{
  "id": 1,
  "title": "Test Post Title",
  "content": "This is the content of a test post",
  "created_at": "2023-05-01T12:34:56.789Z",
  "updated_at": "2023-05-01T12:34:56.789Z",
  "author_id": 1,
  "tags": [
    {
      "id": 1,
      "name": "Technology"
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

## Tag API (API v1)

The following commands require the access_token obtained from the login endpoint.

### 1. Get All Tags

```bash
curl -X GET http://localhost:8000/api/v1/tags/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. Get Specific Tag

```bash
curl -X GET http://localhost:8000/api/v1/tags/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. Get Tag by Name

```bash
curl -X GET http://localhost:8000/api/v1/tags/name/Technology \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Create New Tag

```bash
curl -X POST http://localhost:8000/api/v1/tags/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "name": "New Tag"
  }'
```

### 5. Update Tag

```bash
curl -X PUT http://localhost:8000/api/v1/tags/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "name": "Updated Tag Name"
  }'
```

### 6. Delete Tag

```bash
curl -X DELETE http://localhost:8000/api/v1/tags/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 7. Get Posts Associated with Tag

```bash
curl -X GET http://localhost:8000/api/v1/tags/1/posts \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Response Examples

### Get Tags List Response

```json
[
  {
    "id": 1,
    "name": "Technology"
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

### Get Single Tag Response

```json
{
  "id": 1,
  "name": "Technology"
}
```

### Get Tag Associated Posts Response

```json
{
  "tag": {
    "id": 1,
    "name": "Technology"
  },
  "posts": [
    {
      "id": 1,
      "title": "Test Post Title",
      "content": "This is the content of a test post",
      "created_at": "2023-05-01T12:34:56.789Z",
      "updated_at": "2023-05-01T12:34:56.789Z",
      "author_id": 1,
      "tags": [
        {
          "id": 1,
          "name": "Technology"
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

api_demo.md 文件已经完全翻译成英文版本，包括所有的说明文本、示例数据和响应内容。文件结构和格式保持不变，所有的中文内容都已替换为相应的英文表述。 