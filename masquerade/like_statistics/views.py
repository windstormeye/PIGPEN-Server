from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord
from user.models import MasUser
from blog.models import Blog
from common import utils, decorator


@decorator.request_methon('POST')
@decorator.request_check_args(['content_type', 'object_id', 'masuser_id', 'is_like'])
def like_change(request):
    masuser_id = request.POST.get('masuser_id', '')
    is_like = request.POST.get('is_like', '')
    content_type = request.POST.get('content_type')
    object_id = int(request.POST.get('object_id'))

    masuser = MasUser.objects.get(pk=masuser_id)

    # is_blog
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return utils.ErrorResponse(2333, '点赞文章不存在')

    if is_like == 'true':
        # will like
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, masuser=masuser)
        if created:
            # not like, to like
            # like_num + 1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return utils.SuccessResponse(like_count.liked_num)
        else:
            # did like, not like
            return utils.ErrorResponse(2333, '已点赞过该文章')
    else:
        # cancle like
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, masuser=masuser).exists():
            # did like, cancle like
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, masuser=masuser)
            like_record.delete()
            # like_num - 1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return utils.SuccessResponse(like_count.liked_num)
            else:
                return utils.ErrorResponse(2333, '数据异常')
        else:
            # not liking, cann't cancle like
            return utils.ErrorResponse(2333, '未点赞过该文章')


@decorator.request_methon('GET')
@decorator.request_check_args(['masuser_id'])
def get_like_blog(request):
        masuser_id = request.GET.get('masuser_id', '')

        masuser = MasUser.objects.get(pk=masuser_id)
        like_records = LikeRecord.objects.filter(masuser=masuser)
        final_likes = []
        for like in like_records:
            blog = Blog.objects.get(pk=like.object_id)

            l = {
                'blog': {
                    'masuser': {
                        'nick_name': like.masuser.nick_name,
                    },
                    'content': blog.content,
                    'created_time': blog.created_time.timestamp()
                },
            }
            final_likes.append(l)
        json = {
            'blogs': list(final_likes)
        }
        return utils.SuccessResponse(json)