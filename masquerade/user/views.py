import hashlib
from django.conf import settings
from .models import MasUser
from common import token_utils, utils, decorator, masLogger
from pet.models import Pet
from pet.views import get_pet


@decorator.request_method('POST')
@decorator.request_check_args(['phoneNumber', 'password', 'avatar', 'gender'])
def create_masuser(request):
    phone_number = request.POST.get('phoneNumber')
    # password is a hash_str
    password = request.POST.get('password')
    nick_name = request.POST.get('nick_name')
    avatar = request.POST.get('avatar')
    gender = request.POST.get('gender')

    if MasUser.objects.filter(phone_number=phone_number).exists():
        return utils.ErrorResponse(utils.Code.notFound, request)

    masuser = MasUser.create(phone_number=phone_number, password=password,
                             avatar=avatar, nick_name=nick_name, gender=gender)
    token = token_utils.create_token(masuser.uid)
    json = {
        'masuser': masuser.toJSON(),
        'token': token,
        # 刚注册用户肯定都没有宠物和虚拟宠物
        'feeding_status': [0, 0, 0]
    }

    return utils.SuccessResponse(json, request)


@decorator.request_method('POST')
@decorator.request_check_args(['sign', 'timestamp', 'phoneNumber'])
def login(request):
    phone_number = request.POST.get('phoneNumber')
    sign = request.POST.get('sign')
    timestamp = request.POST.get('timestamp')

    masuser = MasUser.objects.filter(phone_number=phone_number).first()
    if masuser:
        md5 = hashlib.md5()
        md5.update((masuser.password + timestamp).encode('utf-8'))
        masuser_password_hash = md5.hexdigest()

        if sign == masuser_password_hash:
            token = token_utils.create_token(masuser.uid)

            json = {
                'masuser': masuser.toJSON(),
                'token': token,
            }
            return utils.SuccessResponse(json, request)
        else:
            return utils.ErrorResponse(utils.Code.notFound, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('POST')
@decorator.request_check_args([])
def logout(request):
    username = request.POST.get('uid')
    token_utils.delete_token(username)
    json = {
        'isLogOut': 'true'
    }
    return utils.SuccessResponse(json, request)


# 获取用户宠物信息
@decorator.request_method('GET')
@decorator.request_check_args([])
def get_user_pet_info(request):
    uid = request.GET.get('uid')

    # 获取真实宠物信息
    real_pet_array = []
    real_pets = Pet.objects.filter(user__uid=uid)
    for real_pet in real_pets:
        real_pet_array.append(get_pet(real_pet.pet_id, uid))

    json = {
        'pets': real_pet_array,
    }

    return utils.SuccessResponse(json, request)


# 获取用户简单信息
@decorator.request_method('GET')
@decorator.request_check_args(['details_uid'])
def get_user_details(request):
    details_uid = request.GET.get('details_uid')

    user = MasUser.objects.filter(uid=details_uid).first()
    if user:
        json = {
            'masuser': user.toJSON(),
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('POST')
@decorator.request_check_args(['avatar', 'gender'])
def update_user(request):
    uid = request.POST.get('uid')
    nick_name = request.POST.get('nick_name')
    avatar = request.POST.get('avatar')

    user = MasUser.objects.filter(uid=uid).\
        update(avatar=avatar, nick_name=nick_name).first()

    if user:
        json = {
            'masuser': user.toJSON()
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
@decorator.request_check_args([])
def update_token(request):
    uid = request.GET.get('uid')

    token_utils.delete_token(uid)
    token = token_utils.create_token(uid)
    json = {
        'token': token,
    }
    return utils.SuccessResponse(json, request)


@decorator.request_method('GET')
@decorator.request_check_args(['phoneNumber'])
def check_phone(request):
    phone_number = request.GET.get('phoneNumber')

    user = MasUser.objects.filter(phone_number=phone_number).first()

    if user:
        return utils.ErrorResponse(utils.Code.existed, request)
    else:
        json = {
            'status': '可注册'
        }
        return utils.SuccessResponse(json, request)


@decorator.request_method('GET')
@decorator.request_check_args([])
def getRCToken(request):
    from rongcloud import RongCloud

    uid = request.GET.get('uid')
    nick_name = request.GET.get('nick_name')

    app_key = settings.RC_APP_KEY
    app_secret = settings.RC_APP_SECRET
    rcloud = RongCloud(app_key, app_secret)

    r = rcloud.User.getToken(userId=uid,
                             name=nick_name,
                             portraitUri='https://avatars0.githubusercontent.com/u/15074681?s=460&v=4')

    r_json = eval(str(r.response.content, encoding='utf-8'))
    if r_json['code'] == 200:
        json = {
            'token': r_json['token']
        }
        return utils.SuccessResponse(json, request)
    else:
        masLogger.log(request, 2333, str(r.response.content, encoding='utf-8'))
        return utils.ErrorResponse(utils.Code.notFound, request)