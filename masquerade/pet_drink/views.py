import time
from pet_drink.models import PetDrink, PetDrinkLog
from pet.models import Pet
from common import decorator, utils


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id',
                               'water_consume'])
def updateWaterConsume(request):
    """
    更新宠物储水量
    """
    pet_id = request.POST.get('pet_id')
    uid = request.POST.get('uid')
    water_consume = request.POST.get('water_consume')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()

    if pet:
        pet_drink = PetDrink.objects.filter(pet=pet).first()
        if pet_drink:
            pet_drink.water_consume = water_consume
            pet_drink.save()
        else:
            pet_drink = PetDrink(pet=pet,
                                 water_consume=water_consume)
            pet_drink.save()
        return utils.SuccessResponse(pet_drink.toJSON(),
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'pet not exist or not belong you',
                                   request)


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id',
                               'water_residue'])
def updateWaterResidue(request):
    """
    更新宠物剩水量
    """
    pet_id = request.POST.get('pet_id')
    uid = request.POST.get('uid')
    water_residue = request.POST.get('water_residue')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()
    pet_drink = PetDrink.objects.filter(pet=pet).first()
    # 宠物必须存在并且设置过宠物饮水量
    if pet and pet_drink:
        old_time = int(pet_drink.updated_time.timestamp())
        now_time = int(time.time())
        # 上次更新时间到当前时间的间隔秒数
        interval_seconds = now_time - old_time
        # 上次更新时间到当前时间的间隔小时数
        interval_hours = interval_seconds / 3600
        # 间隔小时中需要消耗的水量
        water_total = pet_drink.water_consume * interval_hours
        # 先消耗原有剩余水量
        pet_drink.water_residue -= int(water_total)
        # 后加上此次新增的水量
        pet_drink.water_residue += int(water_residue)
        if pet_drink.water_residue > 0:
            # 剩余水量还可消耗多长时间（秒数）
            time_residue = pet_drink.water_residue / pet_drink.water_consume * 3600
        else:
            # -1 为还是缺水
            # TODO：这里如果是 -1 需要扣分！！！
            time_residue = -1
        pet_drink.save()

        json = pet_drink.toJSON()
        # 预计消耗完的时间
        json['time_finish'] = int(now_time + time_residue)
        return utils.SuccessResponse(json,
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'not pet or not set water_consume for pet',
                                   request)