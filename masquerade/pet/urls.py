from django.urls import path
from . import views

urlpatterns = [
    path('createPet', views.create_pet)
]