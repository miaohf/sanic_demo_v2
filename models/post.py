from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # 一对多关系（一个用户可以有多篇文章）
    author = fields.ForeignKeyField('models.User', related_name='posts')
    
    # 多对多关系
    tags = fields.ManyToManyField('models.Tag', related_name='posts', through='post_tags')

    class Meta:
        table = "posts"

    def __str__(self):
        return self.title


# 创建Pydantic模型
Post_Pydantic = pydantic_model_creator(Post, name="Post")
PostIn_Pydantic = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True) 