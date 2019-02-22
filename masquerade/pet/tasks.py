from virtual_pet.models import virtualPet


def updatePannageTask():
    virtualPetUsers = virtualPet.objects.all()
    for petUser in virtualPetUsers:
        u = petUser.user
        u.money = u.money + 200
        u.save()
    # 查出有虚拟狗的用户 uid
    # 通过 uid 找到猪饲料表记录
    # 叠加对应数据，更新赠送猪饲料字段时间

    # 猪饲料账单
