import datetime

from django.db import models
from pet.models import Pet


class Drink(models.Model):
    """
    「宠物饮水记录」模型
    """
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


class DrinkTarget(models.Model):
    """
    「每日宠物饮水目标」模型
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 宠物每日目标饮水量。默认每日 500 ml（随便写的）
    target = models.IntegerField(default=500)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class DrinkActivity(models.Model):
    """
    「宠物水量预计喝完时间」模型
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 当前水量
    # 整数最多五位数，小数占一位
    current_waters = models.DecimalField(max_digits=5, decimal_places=1)

    created_time = models.DateTimeField(auto_now_add=True)
    # 预计消耗完成时间（时间戳）
    finished_time = models.IntegerField(default=0)


