from django.db import models
from pet.models import Pet
from common import utils


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)


class Blog(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    # 文本内容
    content = models.TextField()
    # 图片内容
    imgs = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_time']

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = 1
        self.save()

    def toJSON(self):
        json = {
            'id': self.id,
            'content': self.content,
            'imgs': utils.create_full_image_url([self.imgs])[0],
            'createdTime': int(self.created_time.timestamp()),
            'updatedTime': int(self.last_updated_time.timestamp())
        }

        return json