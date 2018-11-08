from common import decorator, masLogger
from user.models import MasUser
from common import utils
from .models import Pet, dog_breed, cat_breed
from django.conf import settings


@decorator.request_methon('POST')
@decorator.request_check_args(['nick_name', 'gender', 'pet_type', 'birth_time',
                               'weight', 'ppp_status', 'love_status',
                               'family_relation', 'user_nick_name'])
def create_pet(request):
    nick_name = request.POST.get('nick_name', '')
    gender = request.POST.get('gender', '')
    pet_type = request.POST.get('pet_type', '')
    birth_time = request.POST.get('birth_time', '')
    weight = request.POST.get('weight', '')
    ppp_status = request.POST.get('ppp_status', '')
    love_status = request.POST.get('love_status', '')
    family_relation = request.POST.get('family_relation', '')
    user_nick_name = request.POST.get('user_nick_name', '')

    user = MasUser.objects.filter(nick_name=user_nick_name)

    if user:
        pet = Pet(nick_name=nick_name, gender=gender, pet_type=pet_type,
                  weight=weight, birth_time=birth_time, ppp_status=ppp_status,
                  love_status=love_status, family_relation=family_relation)
        pet.save()

        json = {
            'pet': pet.toJSON(),
        }
        masLogger.log(request, 666)
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse('2333', '用户不存在', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_type'])
def get_breeds(request):
    pet_type = request.GET.get('pet_type', '')
    functions = {
        'dog': dog(),
        'cat': cat()
    }

    if pet_type in functions.keys():
        json = {
            'breeds': functions[pet_type]
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse('2333', '不支持该物种', request)


# 获取所有狗品种
def dog():
    dog_breeds = dog_breed.objects.all()
    breeds = []
    for breed in dog_breeds:
        json = {
            'id': breed.pk,
            'zh_name': breed.zh_name,
        }
        breeds.append(json)
    return breeds


# 获取所有猫品种
def cat():
    cat_breeds = cat_breed.objects.all()
    breeds = []
    for breed in cat_breeds:
        json = {
            'id': breed.pk,
            'zh_name': breed.zh_name,
        }
        breeds.append(json)
    return breeds


# 初始化：尽量通过 python shell 调用该方法
def init_dog_breed():
    f = open(settings.DOG_BREED_DIR, 'r')
    f_str = f.read()
    f_str_arr = f_str.split()
    for dog_name in f_str_arr:
        dog_breed(zh_name=dog_name).save()
    f.close()


# 新增狗品种
def add_dog_breed(breed_name):
    dog_breed(zh_name=breed_name).save()


# 初始化：尽量通过 python shell 调用该方法
def init_cat_breed():
    f = open(settings.CAT_BREED_DIR, 'r')
    f_str = f.read()
    f_str_arr = f_str.split()
    for cat_name in f_str_arr:
        cat_breed(zh_name=cat_name).save()
    f.close()


# 新增猫品种
def add_cat_breed(breed_name):
    cat_breed(zh_name=breed_name).save()



