from django.db import models


class Avatar(models.Model):
    own_id = models.CharField(max_length=10, primary_key=True, db_index=True)
    # 0 => 宠物头像。
    own_type = models.IntegerField(default=0)
    avatar_key = models.CharField(max_length=50)
