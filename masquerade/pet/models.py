from django.db import models
from user.models import MasUser


class Pet(models.Model):
    user_name = models.CharField(unique=True, max_length=8)
    nick_name = models.CharField(unique=True, max_length=18)
    gender = models.IntegerField(default=1)
    pet_type = models.CharField(default='其它', max_length=4)
    # 体重默认为 5 公斤
    weight = models.IntegerField(default=5)
    # 绝育状态默认为 不绝育
    ppp_status = models.IntegerField(default=0)
    # 感情状态默认为 单身
    love_status = models.IntegerField(default=0)
    family_relation = models.IntegerField()
    birth_time = models.CharField(max_length=8)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(MasUser, on_delete=models.CASCADE)

    def toJSON(self):
        from pet_avatar.models import PetAvatar
        if PetAvatar.objects.filter(pet=self).exists():
            avatar_path = PetAvatar.objects.get(pet=self).avatar.url
        else:
            avatar_path = ''
        json = {
            'nick_name': self.nick_name,
            'user_name': self.user_name,
            'pet_type': self.pet_type,
            'weight': self.weight,
            'ppp_status': self.ppp_status,
            'love_status': self.love_status,
            'family_relation': self.family_relation,
            'birth_time': self.birth_time,
            'gender': self.gender,
            'created_time': self.created_time.timestamp(),
            'avatar_path': avatar_path,
        }
        return json


class dog_breed(models.Model):
    zh_name = models.CharField(max_length=50)


class cat_breed(models.Model):
    zh_name = models.CharField(max_length=50)




