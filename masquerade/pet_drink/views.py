from pet_drink.models import PetDrink, PetDrinkLog
from pet.models import Pet
from common import decorator, utils


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id',
                               'water_consume'])
def updateWaterConsume(request):
    """
    更新宠物储水量
    """
    pet_id = request.POST.get('pet_id')
    uid = request.POST.get('uid')
    water_consume = request.POST.get('water_consume')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()

    if pet:
        pet_drink = PetDrink.objects.filter(pet=pet).first()
        if pet_drink:
            pet_drink.water_consume = water_consume
            pet_drink.save()
        else:
            pet_drink = PetDrink(pet=pet,
                                 water_consume=water_consume)
            pet_drink.save()
        return utils.SuccessResponse(pet_drink.toJSON(),
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'pet not exist or not belong you',
                                   request)


@decorator.request_methon('POST')
@decorator.request_check_args(['pet_id', 'water_residue'])
def updateWaterResidue(request):
    """
    更新宠物剩水量
    """
    pet_id = request.POST.get('pet_id')
    uid = request.POST.get('uid')
    water_residue = request.POST.get('water_residue')

    pet = Pet.objects.filter(pet_id=pet_id,
                             user__uid=uid).first()
    pet_drink = PetDrink.objects.filter(pet__pet_id=pet_id).first()
    # 宠物必须存在并且设置过宠物饮水量
    if pet and pet_drink:
        pet_drink = PetDrink.objects.update(pet=pet,
                                            water_residue=water_residue)
        pet_drink.save()
        return utils.SuccessResponse(pet_drink.toJSON(),
                                     request)
    else:
        return utils.ErrorResponse(2333,
                                   'not pet or not set water_consume for pet',
                                   request)
    # TODO：还没测试过


