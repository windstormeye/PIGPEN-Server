from django.db import models
from pet.models import Pet


class PetDrink(models.Model):
    # 关联宠物实体
    pet = models.ForeignKey(Pet,
                            on_delete=models.CASCADE,
                            primary_key=True)
    # 饮水量，默认耗水量为 100ml
    water_consume = models.IntegerField(default=100)
    # 剩水量
    water_residue = models.IntegerField(default=0)
    # 剩余时间 = 储水量 / 耗水量
    time_residue = models.IntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        json = {
            'pet': self.pet.toJSON(),
            'water_consume': self.water_consume,
            'water_residue': self.water_residue,
            'time_residue': self.time_residue,
            'updated_time': int(self.updated_time.timestamp())
        }
        return json


class PetDrinkLog(models.Model):
    # 关联宠物实体
    pet_drink = models.ForeignKey(Pet,
                                  on_delete=models.CASCADE)
    # 此次添加水量
    current_water = models.IntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        json = {
            'pet_drink': self.pet_drink.pk,
            'current_water': self.current_water,
            'updated_time': int(self.updated_time.timestamp()),
        }
        return json
