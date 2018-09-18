from datetime import timezone

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user.models import MasUser


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    masuser = models.ForeignKey(MasUser, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.IntegerField(default=0)

    # 顶级评论（直接获取回复该评论的所有内容）
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # 父级评论
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-comment_time']

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = 1
        self.save()
