from django.core.validators import RegexValidator
from django.db import models


class MasUser(models.Model):
    username = models.CharField(max_length=11, validators=[RegexValidator(r'^\d{1,11}$')], blank=False)
    password = models.CharField(max_length=32, blank=False)

    nick_name = models.CharField(max_length=15, default='')
    # 男 = 0，女 = 1
    gender = models.IntegerField(default=1)
    avatar = models.IntegerField(default=-1)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        # from user_avatar.models import UserAvatar
        # if UserAvatar.objects.filter(masuser=self).exists():
        #     avatar_path = UserAvatar.objects.get(masuser=self).avatar.url
        # else:
        #     avatar_path = ''
        json = {
            'nick_nick': self.nick_name,
            'avatar': self.avatar,
            'gender': self.gender,
            'created_time': self.created_time.timestamp(),
        }
        return json