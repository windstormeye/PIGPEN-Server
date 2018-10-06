from django.db import models
from pet.models import Pet


class PetAvatar(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    # 具体的单个用户头像需要前端自行判断
    avatar = models.ImageField(upload_to='petAvatar', default='')