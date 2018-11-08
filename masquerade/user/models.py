from django.core.validators import RegexValidator
from django.db import models


class MasUser(models.Model):
    username = models.CharField(max_length=11,
                                validators=[RegexValidator(r'^\d{1,11}$')],
                                blank=False,
                                unique=True)
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
            'id': self.pk,
            'nick_name': self.nick_name,
            'avatar': self.avatar,
            'gender': self.gender,
            'created_time': self.created_time.timestamp(),
        }

        return json
