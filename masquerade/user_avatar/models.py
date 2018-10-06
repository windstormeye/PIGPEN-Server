import datetime

from django.db import models
from user.models import MasUser


class UserAvatar(models.Model):
    masuser = models.ForeignKey(MasUser, on_delete=models.CASCADE)
    # 具体的单个用户头像需要前端自行判断
    avatar = models.ImageField(upload_to='userAvatar', default='')