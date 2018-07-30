from django.db import models
from user.models import MasUser


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)


class Blog(models.Model):
    content = models.TextField(default='')
    masuser = models.ForeignKey(MasUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']
