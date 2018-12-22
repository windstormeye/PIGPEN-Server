from django.core.validators import RegexValidator
from django.db import models


class MasUser(models.Model):
    # 用户唯一标识符
    uid = models.CharField(max_length=10, primary_key=True, db_index=True)
    phone_number = models.CharField(max_length=11,
                                    validators=[RegexValidator(r'^\d{1,11}$')],
                                    default='')
    password = models.CharField(max_length=32, blank=False)
    nick_name = models.CharField(max_length=18, unique=True, blank=False)
    # 男 = 0，女 = 1
    gender = models.IntegerField(default=1)
    avatar = models.IntegerField(default=-1)
    # 猪饲料
    money = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        # from user_avatar.models import UserAvatar
        # if UserAvatar.objects.filter(masuser=self).exists():
        #     avatar_path = UserAvatar.objects.get(masuser=self).avatar.url
        # else:
        #     avatar_path = ''
        json = {
            'uid': self.uid,
            'nick_name': self.nick_name,
            'avatar': self.avatar,
            'gender': self.gender,
            'created_time': int(self.created_time.timestamp()),
        }

        return json

    @classmethod
    def create(cls, phone_number='', password='', nick_name='',
               gender='', avatar=''):
        import shortuuid

        shortuuid.set_alphabet('0123456789')
        uid = shortuuid.random(length=10)
        while True:
            if cls.objects.filter(uid=uid).exists():
                uid = shortuuid.random(length=10)
            else:
                break

        return cls.objects.create(uid=uid, phone_number=phone_number,
                                  password=password, nick_name=nick_name,
                                  gender=gender, avatar=avatar)

