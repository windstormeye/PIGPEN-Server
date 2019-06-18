import datetime
from django.shortcuts import render
from .models import CatPlay, CatPlayTarget
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
            (pet_play, created) = CatPlay.objects.get_or_create(pet=pet)

            return utils.SuccessResponse(pet_play.toJSON(), request)
        else:
            pass
    else:
        return utils.ErrorResponse(2333, 'pet not exist', request)
