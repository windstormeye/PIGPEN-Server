from django.urls import path
from . import views

urlpatterns = [
    path('updateWaterConsume', views.updateWaterConsume, name='update_water'),
    path('updateWaterResidu', views.updateWaterResidue, name='update_water'),
]