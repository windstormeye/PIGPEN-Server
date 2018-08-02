import hashlib, time
from .models import MasUser
from common import token_utils, utils, decorator


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
            'masuser_pk': masuser.pk,
            'masuser': {
                'nick_nick': masuser.nick_name,
                'slogan': masuser.slogan,
                'work_mes': masuser.work_mes,
                'interest_mes': masuser.interest_mes,
                'travel_mes': masuser.travel_mes,
                'created_time': masuser.created_time.timestamp(),
            },
            'token': token,
        }
        return utils.SuccessResponse(json)
    else:
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
                    'masuser': {
                        'masuser_id': masuser.id,
                        'username': masuser.nick_name,
                        'slogan': masuser.slogan,
                        'work_mes': masuser.work_mes,
                        'interest_mes': masuser.interest_mes,
                        'travel_mes': masuser.travel_mes,
                        'created_time': masuser.created_time.timestamp(),
                    },
                    'token': token,
                }
                return utils.SuccessResponse(json)
            else:
                return utils.ErrorResponse('2333', '已登录')
        else:
            return utils.ErrorResponse('2333', '密码错误')
    else:
        return utils.ErrorResponse('2333', '已超时')


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