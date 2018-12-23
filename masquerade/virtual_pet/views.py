from user.models import MasUser
from .models import virtualPet
from common import decorator, utils, masLogger


@decorator.request_check_args(['breed', 'gender', 'pet_nick_name'])
@decorator.request_methon('POST')
def create_virtual_pet(request):
    nick_name = request.POST.get('pet_nick_name')
    gender = request.POST.get('gender')
    breed = request.POST.get('breed')
    uid = request.POST.get('uid')

    if virtualPet.objects.filter(nick_name=nick_name).exists():
        return utils.ErrorResponse(2333, '宠物昵称已存在', request)

    user = MasUser.objects.filter(uid=uid).first()
    if user:
        virtual_pet = virtualPet.create(nick_name=nick_name, gender=gender,
                                        breed=breed, user=user)
        json = {
            'virtualPet': virtual_pet.toJSON()
        }

        return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(2333, '用户不存在', request)


@decorator.request_methon('POST')
@decorator.request_check_args([])
def getVirtualPets(request):
    pass
