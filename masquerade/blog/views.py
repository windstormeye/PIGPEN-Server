from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Blog
from user import utils
from user.models import MasUser


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
                    'username': masuser.user.username,
                    'nick_name': masuser.nick_name,
                    'slogan': masuser.slogan,
                    'work_mes': masuser.work_mes,
                    'interest_mes': masuser.interest_mes,
                    'travel_mes': masuser.travel_mes,
                }
                blog['masuser'] = masuser_json
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
