from user.models import MasUser
from .models import virtualPet
from common import decorator, utils, masLogger


@decorator.request_check_args(['breed', 'gender', 'nick_name'])
@decorator.request_methon('POST')
def create_virtual_pet(request):
    nick_name = request.POST.get('nick_name')
    gender = request.POST.get('gender')
    breed = request.POST.get('breed')
    user_nick_name = request.POST.get('user_nick_name')

    user = MasUser.objects.filter(nick_name=user_nick_name).first()

    if user:
        virtual_pet = virtualPet(nick_name=nick_name, gender=int(gender),
                                 breed=int(breed), user=user)
        virtual_pet.save()

        json = {
            'virtualPet': virtual_pet.toJSON()
        }

        masLogger.log(request, 666)
        return utils.SuccessResponse(json)
    else:
        masLogger.log(request, 2333, '用户头像已存在')
        return utils.ErrorResponse(2333, '用户头像已存在')
