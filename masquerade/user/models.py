from django.core.validators import RegexValidator
from django.db import models


class MasUser(models.Model):
    username = models.CharField(max_length=11, validators=[RegexValidator(r'^\d{1,11}$')], blank=False)
    password = models.CharField(max_length=32, blank=False)

    nick_name = models.CharField(max_length=15, default='')
    slogan = models.CharField(max_length=50, default='')
    work_mes = models.CharField(max_length=20, default='')
    interest_mes = models.CharField(max_length=20, default='')
    travel_mes = models.CharField(max_length=20, default='')
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        from user_avatar.models import UserAvatar
        if UserAvatar.objects.filter(masuser=self).exists():
            avatar_path = UserAvatar.objects.get(masuser=self).avatar.url
        else:
            avatar_path = ''
        json = {
            'nick_nick': self.nick_name,
            'slogan': self.slogan,
            'work_mes': self.work_mes,
            'interest_mes': self.interest_mes,
            'travel_mes': self.travel_mes,
            'avatar': avatar_path,
            'created_time': self.created_time.timestamp(),
        }
        return json