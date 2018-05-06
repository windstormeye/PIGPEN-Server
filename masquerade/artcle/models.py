from django.db import models

class artcle(models.Model):
    id          =   models.AutoField(primary_key=True, null=False)
    owner_id    =   models.IntegerField()
    content     =   models.TextField()
    create_time =   models.DateTimeField(auto_now_add=True, null=False)
    update_time =   models.DateTimeField(auto_now=True, null=False)