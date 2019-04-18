from django.db import models
from user.models import MasUser


class Friend(models.Model):
    userA = models.ForeignKey(MasUser,
                              on_delete=models.CASCADE,
                              related_name='userA')
    userB = models.ForeignKey(MasUser,
                              on_delete=models.CASCADE,
                              related_name='userB')
    status = models.IntegerField(default=0)
