from django.contrib.auth.models import User
from .models import MasUser
from common import token_utils, utils, decorator


@decorator.request_methon('POST')
@decorator.request_check_args(['username', 'password'])
def create_masuser(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = User.objects.create_user(username, password)
    user.save()
    masuser = MasUser(user=user)
    masuser.save()

    token = token_utils.create_token(username)
    json = {
        'masuser_pk': masuser.pk,
        'masuser': {
            'user_pk': user.pk,
            'username': user.username,
            'slogan': '',
            'work_mes': '',
            'interest_mes': '',
            'travel_mes': '',
            'created_time': masuser.created_time.timestamp(),
        },
        'token': token,
    }
    return utils.SuccessResponse(json)


@decorator.request_methon('POST')
@decorator.request_check_args(['username', 'password'])
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    masuser = MasUser.objects.get(user__username=username, user__password=password)
    if masuser:
        token = token_utils.get_token(username)
        if not token:
            token = token_utils.create_token(username)
        json = {
            'masuser_pk': masuser.pk,
            'masuser': {
                'user_pk': masuser.user.pk,
                'username': masuser.user.username,
                'slogan': masuser.slogan,
                'work_mes': masuser.work_mes,
                'interest_mes': masuser.interest_mes,
                'travel_mes': masuser.travel_mes,
                'created_time': masuser.created_time.timestamp(),
            },
            'token': token,
        }
        return utils.SuccessResponse(json)


@decorator.request_methon('GET')
@decorator.request_check_args(['username'])
def logout(request):
    username = request.GET.get('username', '')
    token_utils.delete_token(username)
    json = {
        'isLoginout': 'true'
    }
    return utils.SuccessResponse(json)


@decorator.request_methon('POST')
@decorator.request_check_args(['masuser_id', 'nickName', 'slogan', 'work_mes', 'interest_mes', 'travel_mes'])
def update_user(request):
        masuser_pk = request.POST.get('masuser_id', '')
        nick_name = request.POST.get('nickName', '')
        slogan = request.POST.get('slogan', '')
        work_mes = request.POST.get('work_mes', '')
        interest_mes = request.POST.get('interest_mes', '')
        travel_mes = request.POST.get('travel_mes', '')

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
            'created_time': masuser.created_time.timestamp(),
        }
        return utils.SuccessResponse(json)


@decorator.request_methon('GET')
@decorator.request_check_args(['username'])
def update_token(request):
    username = request.GET.get('username')

    token_utils.delete_token(username)
    token = token_utils.create_token(username)
    json = {
        'token': token,
    }
    return utils.SuccessResponse(json)