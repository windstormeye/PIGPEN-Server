from django.db import models
from user.models import MasUser
from avatar.models import Avatar
from common import utils


class Pet(models.Model):
    # 宠物 id
    pet_id = models.IntegerField(unique=True)
    # 宠物昵称
    nick_name = models.CharField(unique=True, max_length=18)
    # 宠物性别: 0 = 女，1 = 男
    gender = models.IntegerField(default=1)
    # 宠物类型：0 = cat, 1 = dog
    pet_type = models.IntegerField(default=0)
    # 体重默认为 5000 克
    weight = models.IntegerField(default=5000)
    # 绝育状态默认为
    # 0 = 未绝育 1 = 已绝育
    ppp_status = models.IntegerField(default=0)
    # 感情状态默认为
    # 0 = 单身 1 = 恋爱 2 = 混乱
    love_status = models.IntegerField(default=0)
    # 宠物生日
    birth_time = models.IntegerField(default=0)
    # 宠物品种
    breed_type = models.CharField(max_length=20)
    # 宠物每日进食重量
    food_weight = models.IntegerField(default=0)
    # 0 平稳 1 一般 2 活跃
    activity = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(MasUser, on_delete=models.CASCADE)

    def toJSON(self):
        json = {
            'nick_name': self.nick_name,
            'pet_id': int(self.pet_id),
            'pet_type': int(self.pet_type),
            'weight': int(self.weight),
            'ppp_status': int(self.ppp_status),
            'love_status': int(self.love_status),
            'birth_time': int(self.birth_time),
            'gender': int(self.gender),
            'breed_type': self.breed_type,
            'created_time': int(self.created_time.timestamp()),
            'activity': int(self.activity),
            'food_weight': int(self.food_weight)
        }

        pet_avatar_key = Avatar.objects.filter(own_id=self.pet_id).first()
        if pet_avatar_key:
            key = pet_avatar_key.avatar_key
            json['avatar_url'] = utils.create_full_image_url([key])[0]

        return json

    @classmethod
    def create(cls, user, pet_nick_name, pet_type, weight, ppp_status, love_status,
               birth_time, gender, breed_type, food_weight, activity):
        """
        创建宠物实体类方法
        :param activity: 宠物运动量
        :param user: 关联的用户
        :param pet_nick_name: 宠物昵称
        :param pet_type: 宠物类型，狗 or 猫
        :param weight: 宠物重量
        :param ppp_status: 宠物绝育情况
        :param love_status: 宠物配偶情况
        :param birth_time: 宠物生日
        :param gender: 宠物性别
        :param breed_type: 宠物种类
        :param food_weight: 宠物每日进食量
        :return: 创建出来的宠物实体
        """
        import shortuuid

        shortuuid.set_alphabet('0123456789')
        pet_id = shortuuid.random(length=8)

        while True:
            if Pet.objects.filter(pet_id=pet_id).exists():
                pet_id = shortuuid.random(length=8)
            else:
                break

        pet = Pet(nick_name=pet_nick_name, pet_id=pet_id, pet_type=pet_type,
                  weight=weight, ppp_status=ppp_status, love_status=love_status,
                  birth_time=birth_time, gender=gender, user=user,
                  breed_type=breed_type, food_weight=food_weight, activity=activity)
        pet.save()
        return pet


class Around(models.Model):
    """
    附近的宠物
    """
    user = models.ForeignKey(MasUser, on_delete=models.CASCADE)

    # 纬度
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    # 经度
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class dog_breed(models.Model):
    """
    狗 种类
    """
    group = models.CharField(max_length=2)
    zh_name = models.CharField(max_length=50)


class cat_breed(models.Model):
    """
    猫 种类
    """
    group = models.CharField(max_length=2)
    zh_name = models.CharField(max_length=50)




