from common import decorator, masLogger
from user.models import MasUser
from common import utils
from .models import Pet


@decorator.request_check_args(['nick_name', 'gender', 'pet_type', 'birth_time',
                               'weight', 'ppp_status', 'love_status',
                               'family_relation', 'user_nick_name'])
@decorator.request_methon('POST')
def create_pet(request):
    nick_name = request.POST.get('nick_name')
    gender = request.POST.get('gender')
    pet_type = request.POST.get('pet_type')
    birth_time = request.POST.get('birth_time')
    weight = request.POST.get('weight')
    ppp_status = request.POST.get('ppp_status')
    love_status = request.POST.get('love_status')
    family_relation = request.POST.get('family_relation')
    user_nick_name = request.POST.get('user_nick_name')

    user = MasUser.objects.filter(nick_name=user_nick_name)

    if user:
        pet = Pet(nick_name=nick_name, gender=gender, pet_type=pet_type,
                  weight=weight, birth_time=birth_time, ppp_status=ppp_status,
                  love_status=love_status, family_relation=family_relation)
        pet.save()

        json = {
            'pet': pet.toJSON(),
        }
        masLogger.log(request, 666)
        return utils.SuccessResponse(json)
    else:
        masLogger.log(request, 2333, '用户不存在')
        return utils.ErrorResponse('2333', '用户不存在')






