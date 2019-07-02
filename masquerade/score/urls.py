from django.urls import path
from . import views

urlpatterns = [
    path('allDrinks', views.drinkGet),
    path('allEats', views.eatGet),
]
