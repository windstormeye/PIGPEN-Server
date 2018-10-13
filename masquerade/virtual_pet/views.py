from user.models import MasUser
from .models import virtualPet
from common import decorator, utils, masLogger
import shortuuid


@decorator.request_check_args(['breed', 'gender', 'nick_name'])
@decorator.request_methon('POST')
def create_virtual_pet(request):
    nick_name = request.POST.get('nick_name')
    gender = request.POST.get('gender')
    breed = request.POST.get('breed')
    user_nick_name = request.POST.get('user_nick_name')

    if virtualPet.objects.filter(nick_name=nick_name).exists():
        masLogger.log(request, 2333, '宠物昵称已存在')
        return utils.ErrorResponse(2333, '宠物昵称已存在')

    user = MasUser.objects.filter(nick_name=user_nick_name).first()
    if user:
        shortuuid.set_alphabet('0123456789')
        pet_id = shortuuid.random(length=8)

        while True:
            if virtualPet.objects.filter(pet_id=pet_id).exists():
                pet_id = shortuuid.random(length=8)
            else:
                break

        virtual_pet = virtualPet(nick_name=nick_name, gender=int(gender),
                                 breed=int(breed), user=user, pet_id=pet_id)
        virtual_pet.save()

        json = {
            'virtualPet': virtual_pet.toJSON()
        }

        masLogger.log(request, 666)
        return utils.SuccessResponse(json)
    else:
        masLogger.log(request, 2333, '用户不存在')
        return utils.ErrorResponse(2333, '用户不存在')
