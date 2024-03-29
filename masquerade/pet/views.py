import pinyin
from django.db.models import Q
from django.conf import settings
from user.models import MasUser
from common import utils, decorator
from .models import Pet, dog_breed, cat_breed, Around
from relationship.models import PetRelationship
from avatar.models import Avatar
from score.models import PetScore
from play.models import DogPlayTarget
from drink.models import Drink


@decorator.request_method('POST')
@decorator.request_check_args(['pet_nick_name', 'gender', 'pet_type',
                               'birth_time', 'weight', 'ppp_status',
                               'love_status', 'relation_code', 'avatar_key',
                               'breed_type', 'food_weight', 'activity'])
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
    avatar_key = request.POST.get('avatar_key')
    breed_type = request.POST.get('breed_type')
    food_weight = request.POST.get('food_weight')
    activity = request.POST.get('activity')

    user = MasUser.objects.filter(uid=uid).first()
    if user:
        # 宠物实体
        pet = Pet.create(pet_nick_name=pet_nick_name,
                         gender=gender,
                         pet_type=pet_type,
                         weight=weight,
                         birth_time=birth_time,
                         love_status=love_status,
                         ppp_status=ppp_status,
                         user=user,
                         breed_type=breed_type,
                         food_weight=food_weight,
                         activity=activity)

        if pet_type == 1:
            # 狗狗每日所需运动卡路里
            DogPlayTarget(pet=pet, target=utils.dogDayTargetKcal(weight)).save()

        # 宠物每日所需饮水量
        Drink(pet=pet, waters=utils.petTargetDrink(pet))

        # 宠物关系实体
        relation = PetRelationship(pet_id=pet.pet_id, uid=uid,
                                   relationship_code=relation_code)
        relation.save()

        # 宠物头像
        Avatar(own_id=pet.pet_id, avatar_key=avatar_key).save()

        pet_json = pet.toJSON()
        pet_json['relationship'] = int(relation.relationship_code)
        return utils.SuccessResponse(pet_json, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
@decorator.request_check_args(['pet_type'])
def get_breeds(request):
    pet_type = request.GET.get('pet_type', '')
    functions = {
        '0': cat(),
        '1': dog()
    }

    if pet_type in functions.keys():
        json = {
            'breeds': functions[pet_type]
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
@decorator.request_check_args(['imageCount'])
def get_pet_upload_avatar_token(request):
    imageCount = int(request.GET.get('imageCount', "1"))

    key = 'pet_avatar'
    jsons = utils.create_upload_image_token(imageCount, key)

    f_json = {
        # list 倒置：不写区间范围的话，默认为原list,因此L[:]和L[::]都表示原list。
        # 根据以上推算，想要倒置list,只需要对原list取负步距-1，即每次回退一个即可得到
        # from: https://blog.csdn.net/akisayaka/article/details/50042175
        'upload_tokens': jsons[::-1]
    }
    return utils.SuccessResponse(f_json, request)


@decorator.request_method('POST')
@decorator.request_check_args(['keys'])
def upload_pet_avatar_key(request):
    keys = request.POST.get('keys')

    keys_array = keys.split(',')

    if keys:
        urls = utils.create_full_image_url(keys_array)
        json = {
            'image_urls': urls
        }
        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
@decorator.request_check_args(['latitude', 'longitude', 'page', 'uid'])
def getAroundPets(request):
    """
    发现附近的猫狗
    """
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    page_num = request.GET.get('page')
    uid = request.GET.get('uid')

    user = MasUser.objects.filter(uid=uid).first()
    if user:
        arounds = utils.get_page_blog_list(Around.objects.filter(~Q(user=user)), page_num)
        pet_json = []

        for around in arounds:
            distance = utils.haversine(float(longitude), float(latitude), around.longitude, around.latitude)
            pets = Pet.objects.filter(user=around.user)

            for pet in pets:
                p_j = {
                    'distance': float('%.1f' % distance),
                    'pet': pet.toJSON()
                }
                pet_json.append(p_j)

        pet_around = Around.objects.filter(user=user).first()
        if pet_around:
            pet_around.latitude = latitude
            pet_around.longitude = longitude
            pet_around.save()
        else:
            Around(user=user, latitude=latitude, longitude=longitude).save()

        return utils.SuccessResponse(pet_json, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
@decorator.request_check_args([])
def get_play_details(request):
    uid = request.GET.get('uid')

    # 获取真实宠物信息
    real_pet_array = []
    real_pets = Pet.objects.filter(user__uid=uid)
    for real_pet in real_pets:
        pet_json = get_pet(real_pet.pet_id, uid)

        (pet, created) = PetScore.objects.get_or_create(pet=real_pet)
        pet_score_json = pet.toJSON()

        p_json = {
            'pet': pet_json,
            'score': pet_score_json
        }

        real_pet_array.append(p_json)

    json = {
        'pets': real_pet_array,
    }

    return utils.SuccessResponse(json, request)


def get_pet(pet_id, uid):
    """
    获取某一宠物全部信息
    :param pet_id: 宠物 id
    :param uid: 用户 id
    :return: 宠物所有相关信息
    """
    pet = Pet.objects.filter(pet_id=pet_id).first()

    if pet:
        pet_relation = PetRelationship.objects.filter(pet_id=pet_id, uid=uid).first()
        if pet_relation:
            pet_json = pet.toJSON()
            pet_json['relationship'] = pet_relation.relationship_code
            (pet_score, created) = PetScore.objects.get_or_create(pet=pet)
            pet_json['score'] = pet_score.toJSON()
            return pet_json


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
