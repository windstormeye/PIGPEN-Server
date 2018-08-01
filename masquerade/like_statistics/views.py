from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord
from user import utils
from user.models import MasUser
from blog.models import Blog


def ErrorResponse(code, message):
    data = {}
    data['msgCode'] = code
    data['msg'] = message
    return JsonResponse(data)


def SuccessResponse(liked_num):
    data = {}
    data['msgCode'] = '666'
    data['liked_num'] = liked_num
    return JsonResponse(data)


def like_change(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        user_name = request.POST.get('user_name', '')
        masuser_id = request.POST.get('masuser_id', '')
        is_like = request.POST.get('is_like', '')
        content_type = request.POST.get('content_type')
        object_id = int(request.POST.get('object_id'))

        if token and user_name and masuser_id and is_like and content_type and object_id:
            if token == utils.get_token(user_name):
                masuser = MasUser.objects.get(pk=masuser_id)

                # is_blog
                try:
                    content_type = ContentType.objects.get(model=content_type)
                    model_class = content_type.model_class()
                    model_obj = model_class.objects.get(pk=object_id)
                except ObjectDoesNotExist:
                    return ErrorResponse(2333, '点赞文章不存在')

                if is_like == 'true':
                    # will like
                    like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, masuser=masuser)
                    if created:
                        # not like, to like
                        # like_num + 1
                        like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
                        like_count.liked_num += 1
                        like_count.save()
                        return SuccessResponse(like_count.liked_num)
                    else:
                        # did like, not like
                        return ErrorResponse(2333, '已点赞过该文章')
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
                            return SuccessResponse(like_count.liked_num)
                        else:
                            return ErrorResponse(2333, '数据异常')
                    else:
                        # not liking, cann't cancle like
                        return ErrorResponse(2333, '未点赞过该文章')
            else:
                return ErrorResponse(1001, 'token失效，请更新')
        else:
            return ErrorResponse(1002, '参数错误')
    else:
        return ErrorResponse(2001, '请求方法错误')


def get_like_blog(request):
    if request.method == 'GET':
        token = request.GET.get('token', '')
        user_name = request.GET.get('user_name', '')
        masuser_id = request.GET.get('masuser_id', '')
        if token and user_name and masuser_id:
            if token == utils.get_token(user_name):
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
                return JsonResponse(json)
            else:
                return ErrorResponse(1001, 'token失效，请更新')
        else:
            return ErrorResponse(1002, '参数错误')
    else:
        return ErrorResponse(2001, '请求方法错误')