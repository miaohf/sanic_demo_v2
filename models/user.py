from tortoise import fields, models
# from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # 反向关系
    posts = fields.ReverseRelation["Post"]

    class Meta:
        table = "users"
    
    def __str__(self):
        return self.username


# # 创建Pydantic模型
# User_Pydantic = pydantic_model_creator(User, name="User")
# UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True) 