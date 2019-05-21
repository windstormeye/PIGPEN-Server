from django.db import models


class PetRelationship(models.Model):
    pet_id = models.CharField(max_length=10, unique=True, db_index=True)
    uid = models.CharField(max_length=10)
    # -1 代表黑户
    #    0       1      2       3      4      5      6       7      8       9      10     11     12
    # ["妈妈", "爸爸", "姥爷", "姥姥", "爷爷", "奶奶", "哥哥", "弟弟", "姐姐", "妹妹" , "叔叔", "阿姨", "其它"]
    relationship_code = models.IntegerField(default=-1)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
