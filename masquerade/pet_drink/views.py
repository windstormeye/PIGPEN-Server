import time
from pet_drink.models import PetDrink, PetDrinkLog
from pet.models import Pet
from common import decorator, utils


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id'])
def petWaterDetails(request):
    """
    获取宠物加水`log`和当前的剩水量
    """
    pet_id = request.GET.get('pet_id')
    uid = request.GET.get('uid')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()
    pet_drink = PetDrink.objects.filter(pet=pet).first()
    if pet and pet_drink:
        json = pet_drink.toJSON()
        logs = []

        # 插入水量卡可供消耗时间
        json['time_finish'] = updatePetDrinkData(pet_drink, 0)

        # 插入加水记录
        pet_drink_logs = PetDrinkLog.objects.filter(pet=pet)
        for log in pet_drink_logs:
            logs.append(log.toJSON())
        json['logs'] = logs

        return utils.SuccessResponse(json,
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'not pet or not set water_consume for pet',
                                   request)


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
        time_residue = updatePetDrinkData(pet_drink, water_residue)

        # 更新宠物饮水记录
        PetDrinkLog(pet=pet, current_water=water_residue).save()
        json = pet_drink.toJSON()

        if time_residue > 0:
            # 预计消耗完的时间
            json['time_finish'] = int(int(time.time()) + time_residue)
        else:
            json['time_finish'] = time_residue

        return utils.SuccessResponse(json,
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'not pet or not set water_consume for pet',
                                   request)


def updatePetDrinkData(pet_drink, water_residue):
    """
    更新 petDrink
    :param pet_drink: 未处理过的原数据对象
    :param water_residue: 需要添加的水
    :return: 处理过的原数据对象
    """

    old_time = int(pet_drink.updated_time.timestamp())
    now_time = int(time.time())
    # 上次更新时间到当前时间的间隔秒数
    interval_seconds = now_time - old_time
    # 上次更新时间到当前时间的间隔小时数
    interval_hours = interval_seconds / 3600
    # 间隔小时中需要消耗的水量
    water_total = pet_drink.water_consume * interval_hours
    # 先消耗原有剩余水量
    # TODO: 这里会出现大负数，怎么处理？
    pet_drink.water_residue -= int(water_total)
    # 后加上此次新增的水量
    pet_drink.water_residue += int(water_residue)
    pet_drink.save()

    if pet_drink.water_residue > 0:
        # 剩余水量还可消耗多长时间（秒数）
        time_residue = pet_drink.water_residue / pet_drink.water_consume * 3600
        # 预计消耗完的时间
        return int(int(time.time()) + time_residue)
    else:

        # -1 为还是缺水
        # TODO：这里如果是 -1 需要扣分！！！
        return -1