from django.db import models


class PetRelationship(models.Model):
    pet_id = models.CharField(max_length=10, unique=True, db_index=True)
    uid = models.CharField(max_length=10)
    # -1 代表黑户
    relationship_code = models.IntegerField(default=-1)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
