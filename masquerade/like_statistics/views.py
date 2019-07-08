from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord
from user.models import MasUser
from blog.models import Blog
from common import utils, decorator


@decorator.request_method('POST')
@decorator.request_check_args(['blog_id', 'is_like'])
def like_change(request):
    uid = request.POST.get('uid')
    is_like = request.POST.get('is_like')
    blog_id = request.POST.get('blog_id')

    masuser = MasUser.objects.filter(uid=uid).first()
    content_type = ContentType.objects.get(model='blog')

    if int(is_like) == 1:
        # will like
        like_record, created = LikeRecord.objects.get_or_create(
            content_type=content_type, object_id=blog_id, masuser=masuser)
        if created:
            # not like, to like
            # like_num + 1
            like_count, created = LikeCount.objects.get_or_create(
                content_type=content_type, object_id=blog_id)
            like_count.liked_num += 1
            like_count.save()

            return utils.SuccessResponse(utils.codeMsg(0), request)
        else:
            return utils.ErrorResponse(utils.Code.existed, request)
    else:
        like_recode = LikeRecord.objects.filter(content_type=content_type,
                                                object_id=blog_id,
                                                masuser=masuser).first()
        if like_recode:
            like_record = LikeRecord.objects.get(content_type=content_type,
                                                 object_id=blog_id,
                                                 masuser=masuser)
            like_record.delete()

            like_count, created = LikeCount.objects.get_or_create(content_type=content_type,
                                                                  object_id=blog_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return utils.SuccessResponse(like_count.liked_num, request)
            else:
                return utils.ErrorResponse(utils.Code.err, request)
        else:
            return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
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
    return utils.SuccessResponse(json, request)