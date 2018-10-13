from django.db import models
from user.models import MasUser


class virtualPet(models.Model):
    nick_name = models.CharField(max_length=18, blank=False, unique=True)
    # 0 => male, 1 => female
    gender = models.IntegerField()
    # 0 => 法国斗牛犬, 1 => 威尔士柯基, 2 => 威玛猎犬
    breed = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    pet_id = models.CharField(max_length=10, unique=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(MasUser, on_delete=models.CASCADE)

    def toJSON(self):
        json = {
            'id': self.pk,
            'nick_name': self.nick_name,
            'gender': self.gender,
            'breed': self.breed,
            'pet_id': self.pet_id,
            'created_time': self.created_time.timestamp(),
        }
        return json
