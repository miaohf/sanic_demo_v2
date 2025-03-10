from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tag(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    
    # 多对多关系的反向引用
    posts = fields.ManyToManyRelation["Post"]

    class Meta:
        table = "tags"

    def __str__(self):
        return self.name


# 创建Pydantic模型
Tag_Pydantic = pydantic_model_creator(Tag, name="Tag")
TagIn_Pydantic = pydantic_model_creator(Tag, name="TagIn", exclude_readonly=True) 