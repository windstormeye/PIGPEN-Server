from common import token_utils, utils, decorator, masLogger
from pet.models import Pet
from drink import views as drink_views
from .models import DrinkDayScore


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id'])
def get(request):
    """
    获取宠物当天评分
    """
    pet_id = request.GET.get('pet_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        drink_views.updateLastWaters(pet, 0)
        current_drink_score = DrinkDayScore.objects.filter(pet=pet).first()
        if current_drink_score:
            return utils.SuccessResponse(current_drink_score.toJSON(), request)
    else:
        return utils.ErrorResponse(2333, 'Not Found', request)


