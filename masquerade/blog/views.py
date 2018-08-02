from django.contrib.contenttypes.models import ContentType
from .models import Blog
from user.models import MasUser
from read_statistics.models import ReadNumber
from like_statistics.models import LikeCount
from comment.models import Comment
from common import utils, decorator


@decorator.request_methon('POST')
@decorator.request_check_args(['content', 'masuser_id'])
def create_blog(request):
    masuserId = request.POST.get('masuser_id', '')
    content = request.POST.get('content', '')
    masuser = MasUser.objects.get(pk=masuserId)

    if not masuser:
        return utils.ErrorResponse(2333, '用户不存在')

    blog = Blog(content=content, masuser=masuser)
    blog.save()

    return utils.SuccessResponse('发布成功')


@decorator.request_methon('GET')
def blog_list(request):
    blogs = Blog.objects.all().values()
    final_blogs = []
    for blog in blogs:
        masuserId = blog['masuser_id']
        masuser = MasUser.objects.get(pk=masuserId)
        masuser_json = {
            'nick_name': masuser.nick_name,
        }
        # replace field `masuser`
        blog['masuser'] = masuser_json

        # get blog read_num
        content_type = ContentType.objects.get(model='blog')
        readnum, create = ReadNumber.objects.get_or_create(content_type=content_type, object_id=blog['id'])
        blog['read_num'] = readnum.read_num

        final_blogs.append(blog)
    json = {
        'blogs': list(final_blogs),
    }
    return utils.SuccessResponse(json)


@decorator.request_methon('GET')
@decorator.request_check_args(['blog_id', 'masuser_id'])
def delete_blog(request):
    masuser_id = request.GET.get('masuser_id', '')
    blog_id = request.GET.get('blog_id', '')
    blog = Blog.objects.get(pk=blog_id)
    # 记得string to int
    if blog.masuser.pk == int(masuser_id):
        Blog.objects.filter(pk=blog_id).delete()
        return utils.SuccessResponse('删除成功')
    else:
        return utils.ErrorResponse(2333, '删除失败，只能删除自己发布的文章')


@decorator.request_methon('GET')
@decorator.request_check_args(['masuser_id'])
def get_user_blog(request):
    userId = request.GET.get('masuser_id', '')

    blogs = Blog.objects.filter(masuser__pk=userId)
    final_blogs = []
    for blog in blogs:
        b = {
            'id': blog.pk,
            'content': blog.content,
            'created_time': blog.created_time,
        }
        final_blogs.append(b)
    if blogs:
        json = {
            'blogs': list(final_blogs)
        }
        return utils.SuccessResponse(json)
    else:
        return utils.ErrorResponse(2333, '该用户未发布文章')


@decorator.request_methon('GET')
@decorator.request_check_args(['content_type', 'object_id'])
def blog_details(request):
    content_type = request.GET.get('content_type', '')
    # blog_id
    object_id = request.GET.get('object_id', '')

    contentType = ContentType.objects.get(model=content_type)
    readnum, create = ReadNumber.objects.get_or_create(content_type=contentType, object_id=object_id)
    readnum.read_num += 1
    readnum.save()
    blog = Blog.objects.get(pk=object_id)

    # get blog like_num
    like_count, created = LikeCount.objects.get_or_create(content_type=contentType, object_id=object_id)

    # get comment_num
    comments = Comment.objects.filter(content_type=contentType, object_id=object_id).count()

    json = {
        'blog': {
            'read_num': readnum.read_num,
            'comment_num': comments,
            'like_num': like_count.liked_num,
            'blog_content': blog.content,
            'blog_created_time': blog.created_time.timestamp(),
        },
        'masuser': {
            'nick_name': blog.masuser.nick_name,
        }
    }
    return utils.SuccessResponse(json)