from django.db import models
from pet.models import Pet


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
            'content': self.content,
            'imgs': self.imgs,
            'created_time': self.created_time,
            'updated_time': self.last_updated_time
        }

        return json