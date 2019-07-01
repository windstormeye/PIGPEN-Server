from common import token_utils, utils, decorator, masLogger
from pet.models import Pet
from .models import DrinkDayScore


@decorator.request_methon('GET')
@decorator.request_check_args(['pet_id'])
def get(request):
    pet_id = request.GET.get('pet_id')

    pet = Pet.objects.filter(pet_id=pet_id).first()
    if pet:
        current_drink_score = DrinkDayScore.objects.filter(pet=pet).first()

    else:
        return utils.ErrorResponse(2333, 'Not Found', request)
