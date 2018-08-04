from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord
from user.models import MasUser
from blog.models import Blog
from common import utils, decorator, masLogger


@decorator.request_methon('POST')
@decorator.request_check_args(['content_type', 'object_id', 'is_like'])
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

            json = {
                'blog_id': object_id,
                'like_num': like_count.liked_num,
            }
            masLogger.log(request, 666)
            return utils.SuccessResponse(json)
        else:
            # did like, not like
            masLogger.log(request, 2333, '已点赞过该文章')
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

                masLogger.log(request, 666)
                return utils.SuccessResponse(like_count.liked_num)
            else:
                masLogger.log(request, 2333, '数据异常')
                return utils.ErrorResponse(2333, '数据异常')
        else:
            # not liking, cann't cancle like
            masLogger.log(request, 2333, '未点赞过该文章')
            return utils.ErrorResponse(2333, '未点赞过该文章')


@decorator.request_methon('GET')
@decorator.request_check_args(['page'])
def get_like_blog(request):
    masuser_id = request.GET.get('masuser_id')
    page_num = request.GET.get('page')

    masuser = MasUser.objects.get(pk=masuser_id)
    likes = LikeRecord.objects.filter(masuser=masuser)

    like_records = utils.get_page_blog_list(likes, page_num)
    final_likes = []
    for like in like_records:
        blog = Blog.objects.get(pk=like.object_id)

        l = {
            'masuser': masuser.toJSON(),
            'content': blog.content,
            'created_time': blog.created_time.timestamp()
        }
        final_likes.append(l)
    json = {
        'blogs': list(final_likes)
    }

    masLogger.log(request, 666)
    return utils.SuccessResponse(json)