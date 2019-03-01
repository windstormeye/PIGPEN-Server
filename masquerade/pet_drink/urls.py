from django.urls import path
from . import views

urlpatterns = [
    path('updateWaterConsume', views.updateWaterConsume, name='updateWaterConsume'),
    path('updateWaterResidu', views.updateWaterResidue, name='updateWaterResidue'),
    path('petWater', views.petWaterDetails, name='petWaterDetails'),
]