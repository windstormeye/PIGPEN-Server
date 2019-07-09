from django.db import models
from user.models import MasUser
from blog.models import Blog


class Collect(models.Model):
    user = models.ForeignKey(MasUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

