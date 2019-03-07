from .models import PetDrinkMarks, PetDrinkWaterDayMarks, PetDrinkWaterHourMarks


def update8HourWaterMarks():
    """更新宠物水量 8：00 分数"""
    pet_water_marks = PetDrinkMarks.objects.all()
    for marks in pet_water_marks:
        PetDrinkWaterHourMarks.objects.update_or_create(pet=pet_water_marks.pet,
                                                        water_8_marks=marks)


def update16HourWaterMarks():
    """更新宠物水量16：00分数"""
    pet_water_marks = PetDrinkMarks.objects.all()
    for marks in pet_water_marks:
        PetDrinkWaterHourMarks.objects.update_or_create(pet=pet_water_marks.pet,
                                                        water_16_marks=marks)


def update24HourWaterMarks():
    """更新宠物水量24：00分数"""
    pet_water_marks = PetDrinkMarks.objects.all()
    for marks in pet_water_marks:
        PetDrinkWaterHourMarks.objects.update_or_create(pet=pet_water_marks.pet,
                                                        water_24_marks=marks)


def updateDayWaterMarks():
    """更新宠物每日水量"""
    # TODO: 如果计算每日水量评分的时间不在 24：00 则可以在这写，否则移到计算 24：00 时刻分数上
    pet_water_marks = PetDrinkWaterHourMarks.objects.all()
    for marks in pet_water_marks:
        day_total_marks = (marks.water_8_marks +
                           marks.water_16_marks +
                           marks.water_24_marks) / 3
        PetDrinkWaterDayMarks(pet=pet_water_marks.pet,
                              water_marks=day_total_marks).save()