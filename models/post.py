from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Post(models.Model):
    """
    Post model representing blog posts or articles.
    
    This model stores content created by users, with relationships
    to the author and associated tags.
    
    Attributes:
        id: Primary key and unique identifier
        title: Title of the post
        content: Main content text of the post
        created_at: Timestamp of post creation
        updated_at: Timestamp of last post update
        author: Foreign key to the User who created the post
        tags: Many-to-many relationship with Tag model
    """
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # One-to-many relationship (a user can have many posts)
    author = fields.ForeignKeyField('models.User', related_name='posts')
    
    # Many-to-many relationship (a post can have many tags, a tag can be on many posts)
    tags = fields.ManyToManyField('models.Tag', related_name='posts', through='post_tags')

    class Meta:
        table = "posts"  # Database table name

    def __str__(self):
        return self.title


# Create Pydantic models for serialization and validation
# Post_Pydantic is used for responses
Post_Pydantic = pydantic_model_creator(Post, name="Post")
# PostIn_Pydantic is used for input data
PostIn_Pydantic = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True) 