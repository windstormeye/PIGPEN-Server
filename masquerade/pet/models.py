from django.db import models
from user.models import MasUser


class Pet(models.Model):
    # 宠物 id
    pet_id = models.CharField(max_length=10, unique=True)
    # 宠物昵称
    nick_name = models.CharField(unique=True, max_length=18)
    # 宠物性别
    gender = models.IntegerField(default=1)
    # 宠物类型：cat/dog
    pet_type = models.CharField(default='其它', max_length=4)
    # 体重默认为 5 公斤
    weight = models.IntegerField(default=5)
    # 绝育状态默认为 不绝育
    ppp_status = models.IntegerField(default=0)
    # 感情状态默认为 单身
    love_status = models.IntegerField(default=0)
    # 宠物生日
    birth_time = models.CharField(max_length=8)
    # 宠物品种
    breed_type = models.CharField(max_length=20)
    # 宠物每日进食重量
    food_weight = models.IntegerField(default=0)
    # 宠物头像
    avatar = models.CharField(max_length=100, default='')
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(MasUser, on_delete=models.CASCADE)

    def toJSON(self):
        json = {
            'nick_name': self.nick_name,
            'pet_id': self.pet_id,
            'pet_type': self.pet_type,
            'weight': self.weight,
            'ppp_status': self.ppp_status,
            'love_status': self.love_status,
            'birth_time': self.birth_time,
            'gender': self.gender,
            'created_time': self.created_time.timestamp(),
            'avatar_path': self.avatar,
        }
        return json

    @classmethod
    def create(cls, user, nick_name, pet_type, weight, ppp_status, love_status,
               birth_time, gender, breed_type, food_weight):
        import shortuuid

        shortuuid.set_alphabet('0123456789')
        pet_id = shortuuid.random(length=8)

        while True:
            if Pet.objects.filter(pet_id=pet_id).exists():
                pet_id = shortuuid.random(length=8)
            else:
                break

        pet = Pet(nick_name=nick_name, pet_id=pet_id, pet_type=pet_type,
                  weight=weight, ppp_status=ppp_status, love_status=love_status,
                  birth_time=birth_time, gender=gender, user=user,
                  breed_type=breed_type, food_weight=food_weight)
        pet.save()
        return pet


class dog_breed(models.Model):
    group = models.CharField(max_length=2)
    zh_name = models.CharField(max_length=50)


class cat_breed(models.Model):
    group = models.CharField(max_length=2)
    zh_name = models.CharField(max_length=50)




