from django.db import models

class User(models.Model):
    id          =   models.AutoField(primary_key=True, null=False)
    username       =   models.CharField(max_length=11, null=False)
    nick_name   =   models.CharField(max_length=15, null=True)
    password   =   models.CharField(max_length=16, null=False)
    status      =   models.CharField(max_length=100, null=True)
    salt        =   models.CharField(max_length=11, null=False)
    create_time =   models.DateTimeField(auto_now_add=True, null=False)
    update_time =   models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'm_user'
