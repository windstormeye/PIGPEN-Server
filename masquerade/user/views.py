import hashlib
from django.conf import settings
from .models import MasUser
from common import token_utils, utils, decorator, masLogger
from virtual_pet.models import virtualPet
from pet.models import Pet
from pet.views import get_pet


@decorator.request_methon('POST')
@decorator.request_check_args(['phoneNumber', 'password', 'avatar', 'gender'])
def create_masuser(request):
    phone_number = request.POST.get('phoneNumber')
    # password is a hash_str
    password = request.POST.get('password')
    nick_name = request.POST.get('nick_name')
    avatar = request.POST.get('avatar')
    gender = request.POST.get('gender')

    if MasUser.objects.filter(phone_number=phone_number).exists():
        return utils.ErrorResponse(2333, 'user exist', request)

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


@decorator.request_methon('POST')
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

            # 喂养状态
            feeding_status = [0, 0, 0]
            if virtualPet.objects.filter(user=masuser).exists():
                feeding_status.insert(2, 1)
            if Pet.objects.filter(user=masuser, pet_type='dog').exists():
                feeding_status.insert(1, 1)
            if Pet.objects.filter(user=masuser, pet_type='cat').exists():
                feeding_status.insert(0, 1)

            json = {
                'masuser': masuser.toJSON(),
                'token': token,
                'feeding_status': feeding_status
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


# 获取用户宠物信息
@decorator.request_methon('GET')
@decorator.request_check_args([])
def get_user_pet_info(request):
    uid = request.GET.get('uid')

    # 获取真实宠物信息
    real_pet_array = []
    real_pets = Pet.objects.filter(user__uid=uid)
    for real_pet in real_pets:
        real_pet_array.append(get_pet(real_pet.pet_id, uid))

    # 获取虚拟宠物信息
    virtual_pet_array = []
    virtual_pets = virtualPet.objects.filter(user__uid=uid)
    for virtual_pet in virtual_pets:
        virtual_pet_array.append(virtual_pet.toJSON())

    json = {
        'real_pet': real_pet_array,
        'virtual_pet': virtual_pet_array
    }

    return utils.SuccessResponse(json, request)


# 获取用户简单信息
@decorator.request_methon('GET')
@decorator.request_check_args(['details_uid'])
def get_user_details(request):
    details_uid = request.GET.get('details_uid')

    user = MasUser.objects.filter(uid=details_uid).first()
    if user:
        # 喂养状态
        feeding_status = [0, 0, 0]
        if virtualPet.objects.filter(user=user).exists():
            feeding_status.insert(2, 1)
        if Pet.objects.filter(user=user, pet_type='dog').exists():
            feeding_status.insert(1, 1)
        if Pet.objects.filter(user=user, pet_type='cat').exists():
            feeding_status.insert(0, 1)

        json = {
            'masuser': user.toJSON(),
            'feeding_status': feeding_status,
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, 'user not exist', request)


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
            'masuser': user.toJSON()
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


@decorator.request_methon('GET')
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
        masLogger.log(request, 2333, r.response.content)
        return utils.ErrorResponse(2333, 'RCToken error', request)