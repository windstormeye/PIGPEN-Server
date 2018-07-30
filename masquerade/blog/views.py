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

