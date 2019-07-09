from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNumber
from like_statistics.models import LikeCount, LikeRecord
from pet.models import Pet
from user.models import MasUser
from blog.models import Blog
from common import utils, decorator
from .models import Collect


@decorator.request_method('GET')
@decorator.request_check_args([])
def get(request):
    uid = request.GET.get('uid')

    final_blogs = []
    collects = Collect.objects.filter(user__uid=uid)
    for collect in collects:
        blog = Blog.objects.filter(pk=collect.blog.pk).first()
        blog_json = {}

        pet = Pet.objects.filter(id=blog.pet.id).first()

        blog_json['pet'] = pet.toJSON()

        blog_content_json = blog.toJSON()

        content_type = ContentType.objects.get(model='blog')
        # 该篇文章的阅读数
        read_num, created = ReadNumber.objects.get_or_create(content_type=content_type,
                                                             object_id=blog.id)
        blog_content_json['readCount'] = read_num.read_num

        # 该篇文章的点赞数
        like_num, created = LikeCount.objects.get_or_create(content_type=content_type,
                                                            object_id=blog.id)
        blog_content_json['likeCount'] = like_num.liked_num

        # 用户是否点赞过
        is_like = LikeRecord.objects.filter(masuser__uid=uid,
                                            content_type=content_type,
                                            object_id=blog.id).first()
        blog_content_json['isLike'] = 0
        if is_like:
            blog_content_json['isLike'] = 1

        # 用户是否收藏过
        is_collect = Collect.objects.filter(user__uid=uid, blog=blog).first()
        blog_content_json['isCollect'] = 0
        if is_collect:
            blog_content_json['isCollect'] = 1

        blog_json['blog'] = blog_content_json
        final_blogs.append(blog_json)

    return utils.SuccessResponse(final_blogs, request)


@decorator.request_method('POST')
@decorator.request_check_args(['blog_id', 'is_collect'])
def post(request):
    uid = request.POST.get('uid')
    blog_id = request.POST.get('blog_id')
    is_collect = request.POST.get('is_collect')

    user = MasUser.objects.filter(uid=uid).first()
    blog = Blog.objects.filter(pk=blog_id).first()
    if user and blog:
        collect = Collect.objects.filter(user=user, blog=blog).first()
        if int(is_collect) == 1:
            if collect:
                return utils.ErrorResponse(utils.Code.existed, request)
            else:
                Collect(user=user, blog=blog).save()
                return utils.SuccessResponse(utils.codeMsg(utils.Code.ok.value), request)
        else:
            if collect:
                collect.delete()
                return utils.SuccessResponse(utils.codeMsg(utils.Code.ok.value), request)
            else:
                return utils.ErrorResponse(utils.Code.notFound, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)