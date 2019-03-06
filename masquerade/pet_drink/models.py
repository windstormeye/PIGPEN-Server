from django.db import models
from pet.models import Pet


class PetDrink(models.Model):
    # 关联宠物实体
    pet = models.OneToOneField(Pet,
                               on_delete=models.CASCADE,
                               primary_key=True)
    # 所需水量
    water_consume = models.IntegerField(default=100)
    # 剩余水量
    water_residue = models.IntegerField(default=0)
    # 每分钟耗水量
    water_consume_min = models.DecimalField(max_digits=4,
                                            decimal_places=2)
    # 最后一次添加水的时间
    add_water_time = models.DateTimeField()
    # 水量消耗完时间
    finish_time = models.DateTimeField()
    updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        json = {
            'pet': self.pet.toJSON(),
            'water_consume': self.water_consume,
            'water_residue': self.water_residue,
            'updated_time': int(self.updated_time.timestamp())
        }
        return json


class PetDrinkLog(models.Model):
    # 关联宠物实体
    pet = models.ForeignKey(Pet,
                            on_delete=models.CASCADE)
    # 此次添加水量
    current_water = models.IntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_time']

    def toJSON(self):
        json = {
            'pet_id': self.pet.pet_id,
            'current_water': self.current_water,
            'updated_time': int(self.updated_time.timestamp()),
        }
        return json
