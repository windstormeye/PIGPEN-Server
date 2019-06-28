from django.db import models
from pet.models import Pet


class Drink(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 本次喝水记录
    waters = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def toJSON(self):
        json = {
            'id': self.id,
            'waters': int(self.waters),
            'created_time': int(self.created_time.timestamp())
        }
        return json


# 每日宠物饮水目标模型
class DrinkTarget(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 宠物每日目标饮水量。默认每日 500 ml（随便写的）
    target = models.IntegerField(default=500)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
