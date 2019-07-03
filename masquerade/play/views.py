import datetime, time
from .models import CatPlay, CatPlayTarget, DogPlay, DogPlayTarget
from pet.models import Pet
from common import utils, decorator


@decorator.request_methon('POST')
@decorator.request_check_args(['durations', 'pet_id', 'pet_type'])
def updateCatPlay(request):
    pet_id = request.POST.get('pet_id')
    durations = request.POST.get('durations')
    pet_type = request.POST.get('pet_type')

    durations = int(durations)

    pet = Pet.objects.filter(pet_id=pet_id).first()

    # 宠物存在
    if pet:
        if int(pet_type) == 0:
            cat_play = CatPlay.objects.filter(pet=pet).first()

            if cat_play:
                today = datetime.date.today().strftime('%d')
                pet_updated_time = cat_play.updated_time.today().strftime('%d')

                # 是否为同一天
                if today == pet_updated_time:
                    cat_play.times += 1
                    cat_play.duration_today += durations

                    cat_play.save()
                    return utils.SuccessResponse('ok', request)

            CatPlay(pet=pet, duration_today=durations, times=1).save()
            return utils.SuccessResponse('ok', request)
        else:
            pass
    else:
        return utils.ErrorResponse(2333, 'pet not exist', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id', 'pet_type'])
def getCatPlay(request):
    pet_id = request.GET.get('pet_id')
    pet_type = request.GET.get('pet_type')

    pet = Pet.objects.filter(pet_id=pet_id).first()

    if pet:
        if int(pet_type) == 0:
            (pet_play, created) = CatPlay.objects.get_or_create(pet=pet, created_time=datetime.date.today())

            return utils.SuccessResponse(pet_play.toJSON(), request)
        else:
            return utils.ErrorResponse(2333, 'pet not cat', request)
    else:
        return utils.ErrorResponse(2333, 'pet not exist', request)


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id', 'play_id', 'pet_type'])
def delete(request):
    """
    删除宠物「玩」记录
    """
    pet_id = request.POST.get('pet_id')
    pet_type = request.POST.get('pet_type')
    play_id = request.POST.get('play_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        # 猫
        if pet_type == 0:
            CatPlay.objects.filter(id=play_id).delete()
            return utils.SuccessResponse('ok', request)
        else:
            DogPlay.objects.filter(id=play_id).delete()
            return utils.SuccessResponse('ok', request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


@decorator.request_methon('POST')
@decorator.request_check_args(['kcal', 'pet_id', 'durations'])
def updateDogPlay(request):
    pet_id = request.POST.get('pet_id')
    kcal = request.POST.get('kcal')
    durations = request.POST.get('durations')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        if int(pet.pet_type) == 1:
            # 每次都新建记录
            DogPlay(pet=pet, kals=kcal, durations=durations).save()
            return utils.SuccessResponse('ok', request)
        else:
            return utils.ErrorResponse(2333, 'pet not dog', request)
    else:
        return utils.ErrorResponse(2333, 'pet not exist', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id', 'page'])
def getDogPlay(request):
    """
    获取所有遛狗数据
    """

    pet_id = request.GET.get('pet_id')
    page_num = request.GET.get('page')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        if pet.pet_type == 1:
            dog_plays = utils.get_page_blog_list(DogPlay.objects.filter(pet=pet), page_num)

            pet_play_jsons = []
            pet_day_play_json = []
            current_day = 0
            current_timestamp = 0

            for pet_play in dog_plays:
                # 新的一天
                if current_day == 0:
                    current_day = pet_play.created_time.day
                    current_timestamp = int(pet_play.created_time.timestamp())
                    pet_day_play_json.append(pet_play.toJSON())
                else:
                    if pet_play.created_time.day == current_day:
                        pet_day_play_json.append(pet_play.toJSON())
                    else:
                        json = {
                            'date': current_timestamp,
                            'plays': pet_day_play_json
                        }
                        pet_play_jsons.append(json)

                        # 清空数据
                        pet_day_play_json = []
                        current_day = 0
                        current_timestamp = int(pet_play.created_time.timestamp())
                        pet_day_play_json.append(pet_play.toJSON())

            # 最后一天
            json = {
                'date': current_timestamp,
                'plays': pet_day_play_json
            }
            pet_play_jsons.append(json)
            return utils.SuccessResponse(pet_play_jsons, request)
        else:
            return utils.ErrorResponse(2333, 'pet not dog', request)
    else:
        return utils.ErrorResponse(2333, 'pet not exist', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id'])
def getDogTodayPlay(request):
    """
    获取当天遛狗所有数据
    """
    pet_id = request.GET.get('pet_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        if pet.pet_type == 1:
            dog_plays = DogPlay.objects.filter(pet=pet, created_time__gt=datetime.date.today())

            final_kcal = 0
            for dog in dog_plays:
                final_kcal += dog.kals

            json = {
                # 遛狗次数
                'times': len(dog_plays),
                # 当天遛狗总卡路里
                'kcal_today': final_kcal,
            }

            dog_target_kcal = DogPlayTarget.objects.filter(pet=pet).first()
            if dog_target_kcal:
                # 该狗的每天所需卡路里
                json['kcal_target_today'] = dog_target_kcal.target
            else:
                # 如果没有数据则创建一次
                dog_target = DogPlayTarget(pet=pet, target=utils.dogDayTargetKcal(pet.weight))
                dog_target.save()

                json['kcal_target_today'] = dog_target.target

            return utils.SuccessResponse(json, request)
