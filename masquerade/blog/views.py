from django.contrib.contenttypes.models import ContentType
from .models import Blog
from pet.models import Pet
from read_statistics.models import ReadNumber
from like_statistics.models import LikeCount
from comment.models import Comment
from common import utils, decorator


@decorator.request_methon('POST')
@decorator.request_check_args(['content', 'imgs', 'petIds'])
def create_blog(request):
    pet_ids = request.POST.get('petIds')
    imgs = request.POST.get('imgs')
    content = request.POST.get('content')

    pet_ids = pet_ids.split(',')
    for pet_id in pet_ids:
        if pet_id != "":
            pet = Pet.objects.filter(pet_id=pet_id).first()
            if pet:
                Blog(pet=pet, content=content, imgs=imgs).save()
            else:
                utils.ErrorResponse(2333, 'Pet Not Found', request)

    return utils.SuccessResponse('ok', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['page'])
def blog_list(request):
    page_num = request.GET.get('page')

    blogs = utils.get_page_blog_list(Blog.objects.filter(is_deleted=0), page_num)
    final_blogs = []
    for blog in blogs:
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

        blog_json['blog'] = blog_content_json

        final_blogs.append(blog_json)

    json = {
        'blogs': list(final_blogs),
    }
    return utils.SuccessResponse(json, request)


@decorator.request_methon('GET')
@decorator.request_check_args(['blog_id'])
def delete_blog(request):
    masuser_id = request.GET.get('masuser_id')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(pk=blog_id)
    # 记得 string to int
    if blog.masuser.pk == int(masuser_id):
        findBlog = Blog.objects.filter(pk=blog_id)
        if findBlog.is_deleted == 0:
            findBlog.delete()
            return utils.SuccessResponse('删除成功', request)
        else:
            return utils.ErrorResponse(2333, '删除失败，文章不存在', request)
    else:
        return utils.ErrorResponse(2333, '删除失败，只能删除自己发布的文章', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['page'])
def get_user_blog(request):
    userId = request.GET.get('masuser_id')
    page_num = request.GET.get('page')

    blogs = utils.get_page_blog_list(Blog.objects.filter(
        masuser__pk=userId, is_deleted=0), page_num)
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
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, '该用户未发布文章', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['content_type', 'object_id'])
def blog_details(request):
    content_type = request.GET.get('content_type', '')
    # blog_id
    object_id = request.GET.get('object_id', '')

    contentType = ContentType.objects.get(model=content_type)
    readnum, create = ReadNumber.objects.get_or_create(
        content_type=contentType, object_id=object_id)
    readnum.read_num += 1
    readnum.save()
    blog = Blog.objects.filter(pk=object_id, is_deleted=0).filter()

    if blog:
        # get blog like_num
        like_count, created = LikeCount.objects.get_or_create(
            content_type=contentType, object_id=object_id)

        # get comment_num
        comments = Comment.objects.filter(content_type=contentType,
                                          object_id=object_id).count()

        json = {
            'blog': {
                'read_num': readnum.read_num,
                'comment_num': comments,
                'like_num': like_count.liked_num,
                'blog_content': blog.content,
                'blog_created_time': blog.created_time.timestamp(),
            },
            'masuser': blog.masuser.toJSON(),
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, '该文章不存在', request)