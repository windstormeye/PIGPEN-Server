import hashlib, time
from .models import MasUser
from common import token_utils, utils, decorator, masLogger


@decorator.request_methon('POST')
@decorator.request_check_args(['username', 'password', 'avatar', 'gender'])
def create_masuser(request):
    username = request.POST.get('username')
    # password is a hash_str
    password = request.POST.get('password')
    timestamp = request.POST.get('timestamp')
    nick_name = request.POST.get('nick_name')
    avatar = request.POST.get('avatar')
    gender = request.POST.get('gender')

    # valid within 5 minutes
    now_timestamp = time.time() / 300
    if (int(int(timestamp) + 300)) > now_timestamp:

        # User'password is another hash_str
        masuser = MasUser(username=username, password=password, avatar=avatar,
                          nick_name=nick_name, gender=gender)
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

        masuser = MasUser.objects.filter(username=username).first()
        if masuser:
            md5 = hashlib.md5()
            md5.update((masuser.password + timestamp).encode('utf-8'))
            masuser_password_hash = md5.hexdigest()

            if sign == masuser_password_hash:

                token = token_utils.create_token(username)
                json = {
                    'masuser': masuser.toJSON(),
                    'token': token,
                }
                masLogger.log(request, 666)
                return utils.SuccessResponse(json)
            else:
                masLogger.log(request, 2333, '密码错误')
                return utils.ErrorResponse(2333, '密码错误')
        else:
            masLogger.log(request, 2333, '用户不存在')
            return utils.ErrorResponse(2333, '用户不存在')
    else:
        masLogger.log(request, 2333, '已超时')
        return utils.ErrorResponse(2333, '已超时')


@decorator.request_methon('GET')
@decorator.request_check_args(['username'])
def logout(request):
    username = request.GET.get('username', '')
    token_utils.delete_token(username)
    json = {
        'isLogOut': 'true'
    }

    masLogger.log(request, 666)
    return utils.SuccessResponse(json)


@decorator.request_methon('POST')
@decorator.request_check_args(['nick_name'])
def get_user_details(request):
    nick_name = request.POST.get('nick_name')

    user = MasUser.objects.filter(nick_name=nick_name).first()
    if user:
        json = {
            'masUser': user.toJSON()
        }

        masLogger.log(request, 666)
        return utils.SuccessResponse(json)
    else:
        masLogger.log(request, 2333, '用户不存在')
        return utils.ErrorResponse(2333, '用户不存在')


@decorator.request_methon('POST')
@decorator.request_check_args(['avatar', 'gender'])
def update_user(request):
    nick_name = request.POST.get('nick_name')
    avatar = request.POST.get('avatar')
    gender = request.POST.get('gender')

    user = MasUser.objects.filter(nick_name=nick_name).update(avatar=avatar,
                                                              gender=gender).first()

    if user:
        json = {
            'masUser': user.toJSON()
        }

        masLogger.log(request, 666)
        return utils.SuccessResponse(json)
    else:
        masLogger.log(request, 2333, '用户不存在')
        return utils.ErrorResponse(2333, '用户不存在')


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


@decorator.request_methon('GET')
@decorator.request_check_args(['phone'])
def check_phone(request):
    phone = request.GET.get('phone')

    user = MasUser.objects.filter(username=phone).first()

    if user:
        masLogger.log(request, 2333, '用户已注册')
        return utils.ErrorResponse(2333, '用户已注册')
    else:
        json = {
            'status': '可注册'
        }
        masLogger.log(request, 666)
        return utils.SuccessResponse(json)
