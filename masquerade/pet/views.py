import pinyin
from django.conf import settings
from common import decorator, masLogger
from user.models import MasUser
from common import utils
from .models import Pet, dog_breed, cat_breed
from relationship.models import PetRelationship


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_nick_name', 'gender', 'pet_type',
                               'birth_time', 'weight', 'ppp_status',
                               'love_status', 'relation_code'])
def create_pet(request):
    pet_nick_name = request.POST.get('pet_nick_name', '')
    gender = request.POST.get('gender', '')
    pet_type = request.POST.get('pet_type', '')
    birth_time = request.POST.get('birth_time', '')
    weight = request.POST.get('weight', '')
    ppp_status = request.POST.get('ppp_status', '')
    love_status = request.POST.get('love_status', '')
    relation_code = request.POST.get('relation_code', -1)
    uid = request.POST.get('uid', '')

    user = MasUser.objects.filter(uid=uid)
    if user:
        # 宠物实体
        pet = Pet.create(nick_name=pet_nick_name, gender=gender,
                         pet_type=pet_type, weight=weight,
                         birth_time=birth_time, love_status=love_status,
                         ppp_status=ppp_status, user=user)
        # 宠物关系实体
        relation = PetRelationship(pet_id=pet.pet_id, uid=uid,
                                   relationship_code=relation_code)

        json = {
            'pet': pet.toJSON(),
            'relationship': relation.relationship_code,
        }
        masLogger.log(request, 666)
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse('2333', 'user not exist', request)


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


@decorator.request_methon('GET')
@decorator.request_check_args(['imageCount'])
def get_pet_upload_avatar_token(request):
    uid = request.GET.get('uid')
    imageCount = int(request.GET.get('imageCount', "1"))

    jsons = utils.create_upload_image_token(imageCount)

    f_json = {
        # list 倒置：不写区间范围的话，默认为原list,因此L[:]和L[::]都表示原list。
        # 根据以上推算，想要倒置list,只需要对原list取负步距-1，即每次回退一个即可得到
        # from: https://blog.csdn.net/akisayaka/article/details/50042175
        'upload_tokens': jsons[::-1]
    }
    return utils.SuccessResponse(f_json, request)


# 获取所有狗品种
def dog():
    dog_breeds = dog_breed.objects.all()
    # 所有种类
    breeds = []
    # 当前种类名
    breed_groups = []
    group = "A"
    for breed in dog_breeds:
        if breed.group != group:
            breed_group = {
                'group': group,
                'breeds': breed_groups,
            }
            breeds.append(breed_group)
            group = breed.group
            breed_groups = []
        b_group = {
            'id': breed.pk,
            'zh_name': breed.zh_name,
        }
        breed_groups.append(b_group)
    return breeds


# 获取所有猫品种
def cat():
    cat_breeds = cat_breed.objects.all()
    # 所有种类
    breeds = []
    # 当前种类名
    breed_groups = []
    group = "A"
    for breed in cat_breeds:
        if breed.group != group:
            breed_group = {
                'group': group,
                'breeds': breed_groups,
            }
            breeds.append(breed_group)
            group = breed.group
            breed_groups = []
        b_group = {
            'id': breed.pk,
            'zh_name': breed.zh_name,
        }
        breed_groups.append(b_group)
    return breeds


# 初始化：尽量通过 python shell 调用该方法
def init_dog_breed():
    f = open(settings.DOG_BREED_DIR, 'r')
    f_str = f.read()
    f_str_arr = f_str.split()
    # 删除 array 中的第一个 'A'
    del f_str_arr[0]
    group = 'A'
    for dog_name in f_str_arr:
        first_cat_name = pinyin.get(dog_name, format='strip')[0:1].upper()
        if first_cat_name != group:
            group = first_cat_name
            # 切换 group 时跳过
            continue
        dog_breed(zh_name=dog_name, group=group).save()

    f.close()


# 新增狗品种
def add_dog_breed(breed_name='未知品种', group='W'):
    dog_breed(zh_name=breed_name, group=group).save()


# 初始化：尽量通过 python shell 调用该方法
def init_cat_breed():
    f = open(settings.CAT_BREED_DIR, 'r')
    f_str = f.read()
    f_str_arr = f_str.split()
    # 删除 array 中的第一个 'A'
    del f_str_arr[0]
    group = 'A'
    for cat_name in f_str_arr:
        first_cat_name = pinyin.get(cat_name, format='strip')[0:1].upper()
        if first_cat_name != group:
            group = first_cat_name
            # 切换 group 时跳过
            continue
        cat_breed(zh_name=cat_name, group=group).save()

    f.close()


# 新增猫品种
def add_cat_breed(breed_name='未知品种', group='W'):
    cat_breed(zh_name=breed_name, group=group).save()



