from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


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
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))