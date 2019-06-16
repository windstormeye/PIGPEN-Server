from django.db import models
from pet.models import Pet


class PetScore(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    food_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)
    water_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)
    play_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)
    happy_s = models.DecimalField(max_digits=3, decimal_places=2, default=8.00)

    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        json = {
            'food_s': float(self.food_s),
            'water_s': float(self.water_s),
            'play_s': float(self.play_s),
            'happy_s': float(self.happy_s)
        }

        return json
