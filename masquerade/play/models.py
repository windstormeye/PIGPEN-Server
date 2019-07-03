from django.db import models
from pet.models import Pet


# 撸猫看板数据模型
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


# 每日撸猫目标模型
class CatPlayTarget(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 默认一小时
    target = models.IntegerField(default=3600)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


# 遛狗看板数据
class DogPlay(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 本次遛狗消耗卡路里
    kals = models.IntegerField(default=0)
    # 本次遛狗持续时间
    durations = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def toJSON(self):
        json = {
            'id': self.id,
            'kcals': int(self.kals),
            'durations': int(self.durations),
        }
        return json


# 每日遛狗目标模型
class DogPlayTarget(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 默认狗狗运动量。默认每日 200 千卡
    target = models.IntegerField(default=200)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
