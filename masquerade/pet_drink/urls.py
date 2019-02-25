from django.urls import path
from . import views

urlpatterns = [
    path('updateWaterResidu', views.updateWaterResidu, name='update_water'),
]