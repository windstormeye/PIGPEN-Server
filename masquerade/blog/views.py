from django.shortcuts import  HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Blog
from user import utils
from user.models import MasUser
from read_statistics.models import ReadNumber
from like_statistics.models import LikeCount


def create_blog(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        masuserId = request.POST.get('masuserId', '')
        masuserName = request.POST.get('masuserName', '')
        content = request.POST.get('content', '')

        if masuserId and content:
            if utils.get_token(masuserName):
                masuser = MasUser.objects.get(pk=masuserId)
                if not masuser:
                    json = {
                        'msgCode': 2333,
                        'msg': '用户不存在',
                    }
                    return HttpResponse(JsonResponse(json))
                blog = Blog(content=content, masuser=masuser)
                blog.save()
                if not blog:
                    json = {
                        'msgCode': 2333,
                        'msg': '文章创建失败',
                    }
                    return HttpResponse(JsonResponse(json))
                json = {
                    'msgCode': 666,
                    'msg': '发布成功',
                }
                return HttpResponse(JsonResponse(json))
            else:
                json = {
                    'msgCode': 1001,
                    'msg': "token失效，请更新",
                }
                return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1002,
                'msg': '参数错误',
            }
            return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def blog_list(request):
    if request.method == 'GET':
        token = request.GET.get('token', '')
        username = request.GET.get('username', '')
        if token == utils.get_token(username):
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

                # get blog like_num
                like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=blog['id'])
                blog['like_num'] = like_count.liked_num

                final_blogs.append(blog)
            json = {
                'blogs': list(final_blogs),
            }
            return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1001,
                'msg': "token失效，请更新",
            }
            return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def delete_blog(request):
    if request.method == 'GET':
        token = request.GET.get('token', '')
        username = request.GET.get('username', '')
        masuser_id = request.GET.get('masuserId', '')
        blog_id = request.GET.get('blogId', '')
        if token and username and masuser_id and blog_id:
            if token == utils.get_token(username):
                blog = Blog.objects.get(pk=blog_id)
                # 记得string to int
                if blog.masuser.pk == int(masuser_id):
                    Blog.objects.filter(pk=blog_id).delete()
                    json = {
                        'msg': '删除成功',
                    }
                    return HttpResponse(JsonResponse(json))
                else:
                    json = {
                        'msgCode': 2333,
                        'msg': '删除失败，只能删除自己发布的文章',
                    }
                    return HttpResponse(JsonResponse(json))
            else:
                json = {
                    'msgCode': 1001,
                    'msg': "token失效，请更新",
                }
                return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1002,
                'msg': "参数错误",
            }
            return HttpResponse(JsonResponse(json))

    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def get_user_blog(request):
    if request.method == 'GET':
        token = request.GET.get('token', '')
        username = request.GET.get('username', '')
        userId = request.GET.get('masuserId', '')
        if token and username and userId:
            if token == utils.get_token(username):
                blogs = Blog.objects.filter(masuser__pk=userId)
                final_blogs = []
                for blog in blogs:
                    b = {
                        'content': blog.content,
                        'created_time': blog.created_time,
                    }
                    final_blogs.append(b)
                if blogs:
                    json = {
                        'blogs': list(final_blogs)
                    }
                    return HttpResponse(JsonResponse(json))
                else:
                    json = {
                        'msgCode': 2333,
                        'msg': '该用户未发布文章'
                    }
                    return HttpResponse(JsonResponse(json))
            else:
                json = {
                    'msgCode': 1001,
                    'msg': "token失效，请更新",
                }
                return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1002,
                'msg': "参数错误",
            }
            return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def blog_details(request):
    if request.method == 'GET':
        token = request.GET.get('token', '')
        username = request.GET.get('user_name', '')
        content_type = request.GET.get('content_type', '')
        # blog_id
        object_id = request.GET.get('object_id', '')

        if token and username and content_type and object_id:
            if token == utils.get_token(username):
                contentType = ContentType.objects.get(model=content_type)
                readnum, create = ReadNumber.objects.get_or_create(content_type=contentType, object_id=object_id)
                readnum.read_num += 1
                readnum.save()
                blog = Blog.objects.get(pk=object_id)
                json = {
                    'blog': {
                        'read_num': readnum.read_num,
                        'blog_content': blog.content,
                        'blog_created_time': blog.created_time.timestamp(),
                    },
                    'masuser': {
                        'nick_name': blog.masuser.nick_name,
                    }
                }
                return HttpResponse(JsonResponse(json))
            else:
                json = {
                    'msgCode': 1001,
                    'msg': "token失效，请更新",
                }
                return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1002,
                'msg': "参数错误",
            }
            return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))