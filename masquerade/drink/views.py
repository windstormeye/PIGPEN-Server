import datetime
from common import utils, decorator
from pet.models import Pet
from .models import Drink, DrinkTarget, DrinkActivity


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id', 'waters'])
def create(request):
    """
    创建宠物 宠物水量
    """
    pet_id = request.POST.get('pet_id')
    waters = request.POST.get('waters')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        Drink(pet=pet, waters=waters).save()
        return utils.SuccessResponse('ok', request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id', 'drink_id', 'waters'])
def update(request):
    """
    更新 宠物水量
    """
    pet_id = request.POST.get('pet_id')
    waters = request.POST.get('waters')
    drink_id = request.POST.get('drink_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        pet_drink = Drink.objects.filter(id=drink_id).first()
        if pet_drink:
            pet_drink.waters = waters
            pet_drink.save()
            return utils.SuccessResponse('ok', request)
        else:
            return utils.ErrorResponse(2333, 'Not Found', request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id', 'page'])
def all(request):
    """
    获取某个宠物历史喝水记录，带分页
    """
    pet_id = request.GET.get('pet_id')
    page_num = request.GET.get('page')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        pet_drinks = utils.get_page_blog_list(Drink.objects.filter(pet=pet), page_num)

        pet_drinks_jsons = []
        pet_day_drinks_json = []
        current_day = 0
        current_timestamp = 0

        for pet_drink in pet_drinks:
            # 新的一天
            if current_day == 0:
                current_day = pet_drink.created_time.day
                current_timestamp = int(pet_drink.created_time.timestamp())
                pet_day_drinks_json.append(pet_drink.toJSON())
            else:
                if pet_drink.created_time.day == current_day:
                    pet_day_drinks_json.append(pet_drink.toJSON())
                else:
                    json = {
                        'date': current_timestamp,
                        'waters': pet_day_drinks_json
                    }
                    pet_drinks_jsons.append(json)

                    # 清空数据
                    pet_day_play_json = []
                    current_day = 0
                    current_timestamp = int(pet_drink.created_time.timestamp())
                    pet_day_play_json.append(pet_drink.toJSON())

        # 最后一天
        json = {
            'date': current_timestamp,
            'waters': pet_day_drinks_json
        }
        pet_drinks_jsons.append(json)
        return utils.SuccessResponse(pet_drinks_jsons, request)
    else:
        return utils.ErrorResponse(2333, 'pet not exist', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id'])
def day(request):
    """
    获取当天宠物饮水所有数据
    """
    pet_id = request.GET.get('pet_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        pet_drinks = Drink.objects.filter(pet=pet, created_time__gt=datetime.date.today())

        final_waters = 0
        for drink in pet_drinks:
            final_waters += drink.waters

        json = {
            # 喝水次数
            'times': len(pet_drinks),
            # 当天宠物喝水总次数
            'water_today': final_waters,
        }

        pet_target_waters = DrinkTarget.objects.filter(pet=pet).first()
        if pet_target_waters:
            # 该宠物的每天所需饮水量
            json['water_target_today'] = pet_target_waters.target
        else:
            # 如果没有数据则创建一次
            pet_target = DrinkTarget(pet=pet, target=utils.petTargetDrink(pet))
            pet_target.save()

            json['water_target_today'] = pet_target.target

        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


def updateLastWaters(pet, waters):
    """
    更新宠物剩余水量
    """

    (drink_activity, created) = DrinkActivity.objects.get_or_create(pet=pet)
    if created:
        # 设置当前剩水量
        drink_activity.current_waters = waters
        # 每分钟消耗量
        expend_waters_min = DrinkTarget.objects.filter(pet=pet).first().target / 3600
        # 可消耗时间间隔
        finished_time_interval = waters * expend_waters_min
        # 可消耗时间
        finished_time = datetime.datetime.now().timestamp() + finished_time_interval
        # 设置「水量预计喝完时间」
        drink_activity.finished_time = finished_time
        # 保存
        drink_activity.save()
    else:
        # 解释：不管是否缺水，只要加了水，分数给满，重新扣分。

        # 判断「水量预计喝完时间」与现在时间戳相比
        # 经过时间戳 = 现在时间戳 - 「水量预计喝完时间」
        # 大于
            # 扣除的分数 = 每分钟耗费分数 * 经过时间戳
            # 入库分数 = 现有分数 - 扣除分数（进「分数记录」表）
            # 更新分数 = 10 分
        # 经过时间里耗费的水量 = 经过时间戳 * 每分钟消耗量
        # 更新剩余水量
        # 当前剩水量 = 原有剩余水量 - 经过时间里耗费的水量
        # 当前剩水量 += 新增水量
        # 更新「水量预计喝完时间」
        pass

