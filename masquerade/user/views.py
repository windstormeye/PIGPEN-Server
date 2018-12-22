import hashlib
from .models import MasUser
from common import token_utils, utils, decorator, masLogger


@decorator.request_methon('POST')
@decorator.request_check_args(['phoneNumber', 'password', 'avatar', 'gender'])
def create_masuser(request):
    phone_number = request.POST.get('phoneNumber')
    # password is a hash_str
    password = request.POST.get('password')
    nick_name = request.POST.get('nick_name')
    avatar = request.POST.get('avatar')
    gender = request.POST.get('gender')

    # User'password is another hash_str
    masuser = MasUser.create(phone_number=phone_number, password=password,
                             avatar=avatar, nick_name=nick_name, gender=gender)
    token = token_utils.create_token(masuser.uid)
    json = {
        'masuser': masuser.toJSON(),
        'token': token,
    }
    print(json)
    return utils.SuccessResponse(json, request)


@decorator.request_methon('POST')
@decorator.request_check_args(['sign', 'timestamp'])
def login(request):
    uid = request.POST.get('uid')
    sign = request.POST.get('sign')
    timestamp = request.POST.get('timestamp')

    masuser = MasUser.objects.filter(uid=uid).first()
    if masuser:
        md5 = hashlib.md5()
        md5.update((masuser.password + timestamp).encode('utf-8'))
        masuser_password_hash = md5.hexdigest()

        if sign == masuser_password_hash:

            token = token_utils.create_token(uid)
            json = {
                'masuser': masuser.toJSON(),
                'token': token,
            }
            return utils.SuccessResponse(json, request)
        else:
            return utils.ErrorResponse(2333, '密码错误', request)
    else:
        return utils.ErrorResponse(2333, '用户不存在', request)


@decorator.request_methon('POST')
@decorator.request_check_args([])
def logout(request):
    username = request.POST.get('uid')
    token_utils.delete_token(username)
    json = {
        'isLogOut': 'true'
    }
    return utils.SuccessResponse(json, request)


@decorator.request_methon('GET')
@decorator.request_check_args(['uid'])
def get_user_details(request):
    nick_name = request.GET.get('uid')

    user = MasUser.objects.filter(nick_name=nick_name).first()
    if user:
        json = {
            'masUser': user.toJSON()
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, '用户不存在', request)


@decorator.request_methon('POST')
@decorator.request_check_args(['avatar', 'gender'])
def update_user(request):
    uid = request.POST.get('uid')
    nick_name = request.POST.get('nick_name')
    avatar = request.POST.get('avatar')

    user = MasUser.objects.filter(uid=uid).\
        update(avatar=avatar, nick_name=nick_name).first()

    if user:
        json = {
            'masUser': user.toJSON()
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, '用户不存在', request)


@decorator.request_methon('GET')
@decorator.request_check_args([])
def update_token(request):
    uid = request.GET.get('uid')

    token_utils.delete_token(uid)
    token = token_utils.create_token(uid)
    json = {
        'token': token,
    }
    return utils.SuccessResponse(json, request)


@decorator.request_methon('GET')
@decorator.request_check_args(['phoneNumber'])
def check_phone(request):
    phone_number = request.GET.get('phoneNumber')

    user = MasUser.objects.filter(phone_number=phone_number).first()

    if user:
        masLogger.log(request, 2333, '用户已注册')
        return utils.ErrorResponse(2333, '用户已注册', request)
    else:
        json = {
            'status': '可注册'
        }
        return utils.SuccessResponse(json, request)
