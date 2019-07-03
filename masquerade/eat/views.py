import datetime
from decimal import Decimal
from common import utils, decorator
from pet.models import Pet
from .models import Eat, EatActivity
from score.models import EatDayScore, EatScore


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id', 'foods'])
def create(request):
    """
    创建 宠物食物
    """
    pet_id = request.POST.get('pet_id')
    foods = request.POST.get('foods')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        Eat(pet=pet, foods=foods).save()
        updateLastFoods(pet, int(foods))

        return utils.SuccessResponse('ok', request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id', 'eat_id'])
def delete(request):
    """
    删除宠物吃饭记录
    """
    pet_id = request.POST.get('pet_id')
    eat_id = request.POST.get('eat_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        Eat.objects.filter(id=eat_id).delete()
        return utils.SuccessResponse('ok', request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id', 'eat_id', 'foods'])
def update(request):
    """
    更新 宠物水量
    """
    pet_id = request.POST.get('pet_id')
    foods = request.POST.get('foods')
    eat_id = request.POST.get('eat_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        pet_eat = Eat.objects.filter(id=eat_id).first()
        if pet_eat:
            pet_eat.foods = foods
            pet_eat.save()
            return utils.SuccessResponse('ok', request)
        else:
            return utils.ErrorResponse(2333, 'Not Found', request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id', 'page'])
def all(request):
    """
    获取某个宠物历史吃饭记录，带分页
    """
    pet_id = request.GET.get('pet_id')
    page_num = request.GET.get('page')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        pet_eats = utils.get_page_blog_list(Eat.objects.filter(pet=pet), page_num)

        pet_eats_jsons = []
        pet_day_eats_json = []
        current_day = 0
        current_timestamp = 0

        for pet_eat in pet_eats:
            # 新的一天
            if current_day == 0:
                current_day = pet_eat.created_time.day
                current_timestamp = int(pet_eat.created_time.timestamp())
                pet_day_eats_json.append(pet_eat.toJSON())
            else:
                if pet_eat.created_time.day == current_day:
                    pet_day_eats_json.append(pet_eat.toJSON())
                else:
                    json = {
                        'date': current_timestamp,
                        'foods': pet_day_eats_json
                    }
                    pet_eats_jsons.append(json)

                    # 清空数据
                    pet_day_eats_json = []
                    current_day = 0
                    current_timestamp = int(pet_eat.created_time.timestamp())
                    pet_day_eats_json.append(pet_eat.toJSON())

        # 最后一天
        json = {
            'date': current_timestamp,
            'foods': pet_day_eats_json
        }
        pet_eats_jsons.append(json)
        return utils.SuccessResponse(pet_eats_jsons, request)
    else:
        return utils.ErrorResponse(2333, 'pet not exist', request)


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id'])
def day(request):
    """
    获取当天宠物吃饭所有数据
    """
    pet_id = request.GET.get('pet_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        pet_eats = Eat.objects.filter(pet=pet, created_time__gt=datetime.date.today())

        final_foods = 0
        for eat in pet_eats:
            final_foods += eat.foods

        json = {
            # 进食次数
            'times': len(pet_eats),
            # 当天宠物进食总数
            'foods_today': final_foods,
            # 当天宠物进食目标
            'food_target_today': pet.food_weight
        }

        # 先更新宠物当前吃饭评分
        updateLastFoods(pet, 0)
        # 查找出宠物当天的分数
        eat_day_score = EatDayScore.objects.filter(pet=pet).first()
        if eat_day_score:
            json['score'] = float(eat_day_score.score)

        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


def updateLastFoods(pet, foods):
    """
    更新宠物剩余饭量
    :param pet:  宠物实体
    :param foods: 当前宠物喂水量。小于 0 则为查分
    """

    (eat_activity, created) = EatActivity.objects.get_or_create(pet=pet)
    # 第一次吃饭的时候不会直接给满 10 分
    if created and foods > 0:
        # 设置当前剩饭量
        eat_activity.current_foods = foods
        # 每分钟消耗量
        expend_foods_min = pet.food_weight / 1440
    else:
        # 判断「水量预计喝完时间」与现在时间戳相比
        now_timestamp = int(datetime.datetime.now().timestamp())
        finished_timestamp = eat_activity.finished_time
        last_updated_timestamp = int(eat_activity.updated_time.timestamp())
        # 经过时间戳 = 现在时间戳 - 上一次更新时间戳
        eat_interval = now_timestamp - last_updated_timestamp

        # 「水量预计喝完时间」是否小于当前时间戳
        if finished_timestamp < now_timestamp:
            # 扣除的分数 = 每分钟耗费分数 * 经过分钟
            deduct_score = (10 / 1440) * (eat_interval / 60)
            # 入库分数 = 现有分数 - 扣除分数（进「分数记录」表）
            (current_eat_score, is_created) = EatDayScore.objects.get_or_create(pet=pet)

            food_score = 10 - deduct_score
            if food_score < 0:
                food_score = 0

            final_write_score = utils.get_two_float(str(food_score), 1)
            # 分数入记录表
            EatScore(pet=pet, score=Decimal(final_write_score)).save()

            if foods > 0:
                # 更新分数 = 10 分
                current_eat_score.score = Decimal(str(10.0))
            else:
                current_eat_score.score = Decimal(str(food_score))
            current_eat_score.save()

        # 经过时间里耗费的食物 = 经过时间戳 * 每分钟消耗量
        expend_foods_min = pet.food_weight / 1440
        expend_foods = eat_interval / 60 * expend_foods_min
        # 当前剩饭量 = 原有剩余食物 - 经过时间里耗费的食物量
        eat_activity.current_foods = float(eat_activity.current_foods) - expend_foods

        # 如果此时小于等于 0
        if eat_activity.current_foods <= 0:
            # 小于 0，就是没吃的了，不管
            eat_activity.current_foods = 0

        if foods > 0:
            # 当前剩饭量 += 新增饭量
            eat_activity.current_foods += foods

    if foods > 0:
        # 更新「食物预计喝完时间」
        # 可消耗时间间隔
        finished_time_interval = foods / expend_foods_min
        # 设置「食物预计喝完时间」
        eat_activity.finished_time += finished_time_interval * 60
        # 保存
        eat_activity.save()

