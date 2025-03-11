from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tag(models.Model):
    """
    Tag model for categorizing posts.
    
    This model represents topic tags that can be associated with posts
    through a many-to-many relationship.
    
    Attributes:
        id: Primary key and unique identifier
        name: Unique name of the tag
        posts: Many-to-many relationship with Post model
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    
    # Many-to-many relationship (reverse reference from Post model)
    posts = fields.ManyToManyRelation["Post"]

    class Meta:
        table = "tags"  # Database table name

    def __str__(self):
        return self.name


# Create Pydantic models for serialization and validation
# Tag_Pydantic is used for responses
Tag_Pydantic = pydantic_model_creator(Tag, name="Tag")
# TagIn_Pydantic is used for input data
TagIn_Pydantic = pydantic_model_creator(Tag, name="TagIn", exclude_readonly=True) 