from django.db import models
from user.models import MasUser


class virtualPet(models.Model):
    nick_name = models.CharField(max_length=18, blank=False, unique=True)
    # 0 => male, 1 => female
    gender = models.IntegerField()
    # 0 => 法国斗牛犬, 1 => 威尔士柯基, 2 => 威玛猎犬
    breed = models.IntegerField()
    pet_id = models.CharField(max_length=10, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(MasUser, on_delete=models.CASCADE)

    def toJSON(self):
        json = {
            'nick_name': self.nick_name,
            'gender': self.gender,
            'breed': self.breed,
            'pet_id': self.pet_id,
            'created_time': int(self.created_time.timestamp()),
        }
        return json

    @classmethod
    def create(cls, user, nick_name='', gender='', breed=''):
        import shortuuid

        shortuuid.set_alphabet('0123456789')
        pet_id = shortuuid.random(length=8)

        while True:
            if virtualPet.objects.filter(pet_id=pet_id).exists():
                pet_id = shortuuid.random(length=8)
            else:
                break

        return cls.objects.create(nick_name=nick_name, gender=int(gender),
                                  breed=int(breed), user=user, pet_id=pet_id)
