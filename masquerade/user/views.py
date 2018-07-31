from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import MasUser
from . import utils


def create_masuser(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = User.objects.create_user(username, password)
        user.save()
        masuser = MasUser(user=user)
        masuser.save()

        token = utils.create_token(username)
        json = {
            'masuser_pk': masuser.pk,
            'masuser': {
                'user_pk': user.pk,
                'username': user.username,
                'slogan': '',
                'work_mes': '',
                'interest_mes': '',
                'travel_mes': '',
                'created_time': masuser.created_time,
                'last_updated_time': masuser.last_updated_time,
            },
            'token': token,
        }
        return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        masuser = MasUser.objects.get(user__username=username, user__password=password)
        if masuser:
            token = utils.get_token(username)
            if not token:
                token = utils.create_token(username)
            json = {
                'masuser_pk': masuser.pk,
                'masuser': {
                    'user_pk': masuser.user.pk,
                    'username': masuser.user.username,
                    'slogan': masuser.slogan,
                    'work_mes': masuser.work_mes,
                    'interest_mes': masuser.interest_mes,
                    'travel_mes': masuser.travel_mes,
                    'created_time': masuser.created_time,
                    'last_updated_time': masuser.last_updated_time,
                },
                'token': token,
            }
            return HttpResponse(JsonResponse(json))

    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def logout(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        utils.delete_token(username)
        return HttpResponse(JsonResponse({'islogout': 'true'}))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def update_user(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        username = request.POST.get('username', '')
        masuser_pk = request.POST.get('masuser_pk', '')
        nick_name = request.POST.get('nickName', '')
        slogan = request.POST.get('slogan', '')
        work_mes = request.POST.get('work_mes', '')
        interest_mes = request.POST.get('interest_mes', '')
        travel_mes = request.POST.get('travel_mes', '')

        if utils.get_token(username) == token:
            MasUser.objects.filter(pk=masuser_pk).update(slogan=slogan, work_mes=work_mes, interest_mes=interest_mes,
                                                         travel_mes=travel_mes, nick_name=nick_name)
            masuser = MasUser.objects.get(pk=masuser_pk)
            json = {
                'masuser_pk': masuser.pk,
                'nick_name': masuser.nick_name,
                'slogan': masuser.slogan,
                'work_mes': masuser.work_mes,
                'interest_mes': masuser.interest_mes,
                'travel_mes': masuser.travel_mes,
                'created_time': masuser.created_time,
                'last_updated_time': masuser.last_updated_time,
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


def update_token(request):
    if request.method == 'GET':
        username = request.GET.get('username')

        utils.delete_token(username)
        token = utils.create_token(username)
        json = {
            'token': token,
        }
        return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))