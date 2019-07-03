from django.db import models
from pet.models import Pet


class Eat(models.Model):
    """
    「宠物吃饭记录」模型
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 本次吃饭记录
    foods = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def toJSON(self):
        json = {
            'id': self.id,
            'foods': int(self.foods),
            'created_time': int(self.created_time.timestamp())
        }
        return json


class EatActivity(models.Model):
    """
    「宠物食物预计吃完时间」模型
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    # 当前食物
    # 整数最多五位数，小数占一位
    current_foods = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    # 预计消耗完成时间（时间戳）
    finished_time = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
