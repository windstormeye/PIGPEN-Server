from django.db import models
from pet.models import Pet


class CatPlay(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    times = models.IntegerField(default=0)
    duration_today = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        json = {
            'times': int(self.times),
            'duration_today': int(self.duration_today),
            'created_time': int(self.created_time.timestamp()),
            'update_time': int(self.updated_time.timestamp())
        }

        return json


class CatPlayTarget(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 默认一小时
    target = models.IntegerField(default=3600)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class DogPlay(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 今日遛狗次数
    times = models.IntegerField(default=0)
    # 今日消耗卡路里
    kals_today = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class DogPlayLog(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 今日遛狗次数
    times = models.IntegerField(default=0)
    # 今日消耗卡路里
    kals_today = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)