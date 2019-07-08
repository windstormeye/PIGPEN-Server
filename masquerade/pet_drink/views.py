import time
from pet_drink.models import PetDrink, PetDrinkLog, PetDrinkMarks, PetDrinkWaterHourMarks
from pet.models import Pet
from common import decorator, utils


@decorator.request_method('GET')
@decorator.request_check_args(['pet_id'])
def petWaterDetails(request):
    """获取宠物水量详情：当前分数、当前时间段分数、当前剩水量、预期消耗完时间、log"""

    pet_id = request.GET.get('pet_id')
    uid = request.GET.get('uid')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()
    pet_drink = PetDrink.objects.filter(pet=pet).first()
    if pet and pet_drink:
        pet_drink = updateWaterData(pet_drink)

        # 当前剩水量、预期消耗完时间
        json = pet_drink.toJSON()

        # 插入加水记录
        logs = []
        pet_drink_logs = PetDrinkLog.objects.filter(pet=pet)
        for log in pet_drink_logs:
            logs.append(log.toJSON())
        json['logs'] = logs

        # 当前分数
        pet_current_water_marks = PetDrinkMarks.objects.filter(pet=pet).first()
        if pet_current_water_marks:
            json['current_marks'] = pet_current_water_marks.toJSON()

        # 当前时间段分数
        pet_hour_water_marks = PetDrinkWaterHourMarks.objects.filter(pet=pet).filter()
        if pet_hour_water_marks:
            json['hour_marks'] = pet_hour_water_marks.toJSON()

        return utils.SuccessResponse(json,
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'not pet or not set water_consume for pet',
                                   request)


@decorator.request_method('POST')
@decorator.request_check_args(['pet_id',
                               'water_consume'])
def updateWaterConsume(request):
    """更新宠物储水量"""

    pet_id = request.POST.get('pet_id')
    uid = request.POST.get('uid')
    # 每小时进水量
    water_consume = request.POST.get('water_consume')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()

    if pet:
        pet_drink = PetDrink.objects.filter(pet=pet).first()
        # 转化成每分钟进水量
        water_consume_min = water_consume / 60
        if pet_drink:
            pet_drink.water_consume = water_consume
            pet_drink.water_consume_min = water_consume_min
            pet_drink.save()
        else:
            pet_drink = PetDrink(pet=pet,
                                 water_consume=water_consume,
                                 water_consume_min=water_consume_min)
            pet_drink.save()
        return utils.SuccessResponse(pet_drink.toJSON(),
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'pet not exist or not belong you',
                                   request)


@decorator.request_method('POST')
@decorator.request_check_args(['pet_id',
                               'water_residue'])
def updateWaterResidue(request):
    """更新宠物剩水量"""

    pet_id = request.POST.get('pet_id')
    uid = request.POST.get('uid')
    water_residue = request.POST.get('water_residue')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()
    pet_drink = PetDrink.objects.filter(pet=pet).first()
    # 宠物必须存在并且设置过宠物饮水量
    if pet and pet_drink:
        now_time = int(time.time())
        total_water_residue = pet_drink.water_residue + water_residue
        # 得到可供消耗的秒数
        finish_time = total_water_residue / pet_drink.water_consume_min * 60
        # 更新未来水量耗尽时间
        pet_drink.finish_time = now_time + finish_time
        pet_drink.water_residue = total_water_residue
        pet_drink.add_water_time = now_time

        updateWaterData(pet_drink)
        # 添加水量记录
        PetDrinkLog(pet=pet,
                    current_water=water_residue).save()

        json = pet_drink.toJSON()
        json['time_finish'] = pet_drink.finish_time

        return utils.SuccessResponse(json,
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'not pet or please set water_consume for pet',
                                   request)


def updateWaterData(pet_drink):
    """更新宠物水量数据和水量分数"""
    now_time = int(time.time())
    add_water_time = pet_drink.add_water_time
    # 跨度时间 = 当前时间 - 加水时间
    span_time_min = (now_time - add_water_time) / 60
    # 跨度时间中需要消耗的水量
    span_water = span_time_min * pet_drink.water_consume_min
    # 当前剩水量 = 宠物剩水量 - 跨度时间中需要消耗的水量
    current_water = pet_drink.water_residue - span_water

    if current_water > 0:
        pet_drink.water_residue = current_water
    else:
        pet_drink.water_residue = 0

        # 扣分
        # 超出时间（分钟） = 当前时间 - 水量消耗完时间
        out_time_min = (now_time - pet_drink.finish_time) / 60
        # 需要扣的分
        # 0.07 = 10分 / 60min
        deduct_marks = out_time_min * 0.07
        PetDrinkMarks.objects.update_or_create(pet=pet_drink.pet,
                                               water_marks=deduct_marks)
    pet_drink.save()
    return pet_drink






