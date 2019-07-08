from common import token_utils, utils, decorator, masLogger
from pet.models import Pet
from drink import views as drink_views
from eat import views as eat_views
from .models import DrinkDayScore, EatDayScore


@decorator.request_method('GET')
@decorator.request_check_args(['pet_id'])
def drinkGet(request):
    """
    获取宠物当天喝水评分
    """
    pet_id = request.GET.get('pet_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        drink_views.updateLastWaters(pet, 0)
        current_drink_score = DrinkDayScore.objects.filter(pet=pet).first()
        if current_drink_score:
            return utils.SuccessResponse(current_drink_score.toJSON(), request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
@decorator.request_check_args(['pet_id'])
def eatGet(request):
    """
    获取宠物当天吃饭评分
    """
    pet_id = request.GET.get('pet_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        eat_views.updateLastFoods(pet, 0)
        current_eat_score = EatDayScore.objects.filter(pet=pet).first()
        if current_eat_score:
            return utils.SuccessResponse(current_eat_score.toJSON(), request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)