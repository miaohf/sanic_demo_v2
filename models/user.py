from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    """
    User model representing application users.
    
    This model stores user account information including authentication
    and basic profile data.
    
    Attributes:
        id: Primary key and unique identifier
        username: Unique username for the account
        email: Unique email address for the account
        password_hash: Hashed password for authentication
        is_active: Flag indicating if the account is active
        created_at: Timestamp of account creation
        updated_at: Timestamp of last account update
    """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # Reverse relation to posts (defined in Post model)
    posts = fields.ReverseRelation["Post"]

    class Meta:
        table = "users"  # Database table name
    
    def __str__(self):
        return self.username


# Create Pydantic models for serialization and validation
# User_Pydantic is used for responses (excludes password_hash)
User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password_hash",))
# UserIn_Pydantic is used for input data (excludes auto-generated fields)
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True) 