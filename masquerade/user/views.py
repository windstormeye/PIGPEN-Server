import hashlib, time
from .models import MasUser
from user_avatar.models import UserAvatar
from common import token_utils, utils, decorator, masLogger


@decorator.request_methon('POST')
@decorator.request_check_args(['username', 'password', 'timestamp'])
def create_masuser(request):
    username = request.POST.get('username', '')
    # password is a hash_str
    password = request.POST.get('password', '')
    timestamp = request.POST.get('timestamp', '')

    # valid within 5 minutes
    now_timestamp = time.time() / 300
    if (int(int(timestamp) + 300)) > now_timestamp:

        # User'password is another hash_str
        masuser = MasUser(username=username, password=password)
        masuser.save()

        token = token_utils.create_token(username)
        json = {
            'masuser_id': masuser.pk,
            'masuser': masuser.toJSON(),
            'token': token,
        }
        masLogger.log(request, 666)
        return utils.SuccessResponse(json)
    else:
        masLogger.log(request, 2333, '已超时')
        return utils.ErrorResponse('2333', '已超时')


@decorator.request_methon('POST')
@decorator.request_check_args(['username', 'sign', 'timestamp'])
def login(request):
    username = request.POST.get('username', '')
    sign = request.POST.get('sign', '')
    timestamp = request.POST.get('timestamp', '')

    # valid within 5 minutes
    now_timestamp = time.time() / 300
    if (int(timestamp) + 300) > now_timestamp:

        masuser = MasUser.objects.get(username=username)

        md5 = hashlib.md5()
        md5.update((masuser.password + timestamp).encode('utf-8'))
        masuser_password_hash = md5.hexdigest()

        if sign == masuser_password_hash:
            token = token_utils.get_token(username)
            if not token:
                token = token_utils.create_token(username)
                json = {
                    'masuser': masuser.toJSON(),
                    'token': token,
                }
                masLogger.log(request, 666)
                return utils.SuccessResponse(json)
            else:
                masLogger.log(request, 2333, '已登录')
                return utils.ErrorResponse(2333, '已登录')
        else:
            masLogger.log(request, 2333, '密码错误')
            return utils.ErrorResponse(2333, '密码错误')
    else:
        masLogger.log(request, 2333, '已超时')
        return utils.ErrorResponse(2333, '已超时')


@decorator.request_methon('GET')
@decorator.request_check_args(['username'])
def logout(request):
    username = request.GET.get('username', '')
    token_utils.delete_token(username)
    json = {
        'isLoginout': 'true'
    }

    masLogger.log(request, 666)
    return utils.SuccessResponse(json)


@decorator.request_methon('POST')
@decorator.request_check_args([])
def get_user_details(request):
    masuser_id = request.POST.get('masuser_id')

    masuser = MasUser.objects.get(pk=masuser_id)

    json = {
        'masuser': masuser.toJSON()
    }

    masLogger.log(request, 666)
    return utils.SuccessResponse(json)


@decorator.request_methon('POST')
@decorator.request_check_args(['slogan', 'work_mes', 'interest_mes', 'travel_mes'])
def update_user(request):
    masuser_pk = request.POST.get('masuser_id', '')
    nick_name = request.POST.get('nick_name', '')
    slogan = request.POST.get('slogan', '')
    work_mes = request.POST.get('work_mes', '')
    interest_mes = request.POST.get('interest_mes', '')
    travel_mes = request.POST.get('travel_mes', '')

    MasUser.objects.filter(pk=masuser_pk).update(slogan=slogan, work_mes=work_mes, interest_mes=interest_mes,
                                                 travel_mes=travel_mes, nick_name=nick_name)
    masuser = MasUser.objects.get(pk=masuser_pk)
    json = {
        'masuser': masuser.toJSON()
    }

    masLogger.log(request, 666)
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

    masLogger.log(request, 666)
    return utils.SuccessResponse(json)