from django.db import models
from pet.models import Pet


class PetScore(models.Model):
    """
    娱乐圈-首页-宠物看板分数
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    food_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)
    water_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)
    play_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)
    happy_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)

    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        json = {
            'food_s': float(self.food_s),
            'water_s': float(self.water_s),
            'play_s': float(self.play_s),
            'happy_s': float(self.happy_s)
        }

        return json


class DrinkScore(models.Model):
    """
    宠物喝水评分总记录
    """

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    # 只保留两位小数
    score = models.DecimalField(max_digits=2, decimal_places=1, default=8.0)

    created_time = models.DateTimeField(auto_now_add=True)


class DrinkDayScore(models.Model):
    """
    宠物当天喝水评分记录
    """

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    # 当前分数
    score = models.DecimalField(max_digits=3, decimal_places=1, default=8.0)
    # 第一个时间段
    first_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    # 第二个时间段
    second_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    # 第三个时间段
    third_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    created_time = models.DateTimeField(auto_now_add=True)
