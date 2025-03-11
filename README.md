# Sanic Demo Project

This is a RESTful API example project based on Sanic, demonstrating how to build a full-featured backend application using the Sanic framework.

## Features

- **Tortoise ORM** for database operations, supporting one-to-many and many-to-many relationships
- **Pydantic** for data validation and serialization
- **JWT** authentication with automatic token refresh
- **API version control** (v1/v2)
- Modular code organization using Sanic Blueprints

## Project Structure

```
├── app.py                     # Main application entry point
├── config.py                  # Configuration file
├── models/                    # Tortoise ORM data models
│   ├── __init__.py
│   ├── user.py                # User model
│   ├── post.py                # Post model (one-to-many relation)
│   └── tag.py                 # Tag model (many-to-many relation)
├── schemas/                   # Pydantic schemas
│   ├── __init__.py
│   ├── user.py
│   ├── post.py
│   └── token.py
├── apps/                      # Route groups
│   ├── __init__.py
│   ├── api_v1/                # API v1 version
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── tags.py
│   ├── api_v2/                # API v2 version
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── tags.py
│   └── auth/                  # Authentication module
│       ├── __init__.py
│       └── routes.py
├── middlewares/               # Middleware
│   ├── __init__.py
│   └── auth.py                # JWT authentication middleware
└── services/                  # Business logic
    ├── __init__.py
    └── auth.py                # Authentication service
```

## Technology Stack

- [Sanic](https://sanic.dev/) - Asynchronous Python web framework
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/) - Asynchronous ORM framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation and serialization library
- [PyJWT](https://pyjwt.readthedocs.io/) - JWT implementation
- [Passlib](https://passlib.readthedocs.io/) - Password hashing library

## Installation and Startup

### Prerequisites

- Python 3.8+
- pip

### Installing Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install sanic tortoise-orm pydantic[email] passlib[bcrypt] pyjwt
```

### Starting the Application

```bash
python app.py
```

By default, the application will run at http://0.0.0.0:8000.

## API Documentation

### Authentication Endpoints

| Method | Path | Description |
|--------|------|------------|
| POST | /auth/register | Register a new user |
| POST | /auth/login | User login |
| POST | /auth/refresh | Refresh access token |

### User Endpoints (API v1)

| Method | Path | Description |
|--------|------|------------|
| GET | /api/v1/users/ | Get all users |
| GET | /api/v1/users/\<user_id\> | Get a specific user |
| GET | /api/v1/users/me | Get current user info |
| PUT | /api/v1/users/me | Update current user |

### Post Endpoints (API v1)

| Method | Path | Description |
|--------|------|------------|
| GET | /api/v1/posts/ | Get all posts |
| POST | /api/v1/posts/ | Create a new post |
| GET | /api/v1/posts/\<post_id\> | Get a specific post |
| PUT | /api/v1/posts/\<post_id\> | Update a post |
| DELETE | /api/v1/posts/\<post_id\> | Delete a post |

### Tag Endpoints (API v1)

| Method | Path | Description |
|--------|------|------------|
| GET | /api/v1/tags/ | Get all tags |
| POST | /api/v1/tags/ | Create a new tag |
| GET | /api/v1/tags/\<tag_id\> | Get a specific tag |
| PUT | /api/v1/tags/\<tag_id\> | Update a tag |
| DELETE | /api/v1/tags/\<tag_id\> | Delete a tag |
| GET | /api/v1/tags/\<tag_id\>/posts | Get posts for a tag |
| GET | /api/v1/tags/name/\<tag_name\> | Get tag by name |

API v2 provides the same endpoints under the `/api/v2/` path.

## Data Model Relationships

- **User** and **Post**: One-to-many relationship
- **Post** and **Tag**: Many-to-many relationship

## Authentication Flow

1. User registers via `/auth/register` or logs in via `/auth/login`
2. Upon successful authentication, the server returns an `access_token` and `refresh_token`
3. The client includes `Bearer <access_token>` in the `Authorization` header for subsequent requests
4. When the `access_token` expires, use `/auth/refresh` with the `refresh_token` to get a new `access_token`

## Development and Extension

### Adding a New API Version

1. Create a new version directory under `apps/` (e.g., `api_v3/`)
2. Register the new version blueprint in `app.py`

### Adding New Entity Models

1. Create a new model file in the `models/` directory
2. Add the new model to the `MODELS` list in `config.py`
3. Create corresponding Pydantic models in the `schemas/` directory
4. Create route handlers in the appropriate API version directory

## License

[MIT License](LICENSE)
