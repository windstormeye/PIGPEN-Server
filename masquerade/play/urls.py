from django.urls import path
from . import views

urlpatterns = [
    path('cat', views.getCatPlay),
    path('updateCat', views.updateCatPlay),
    path('dog', views.getDogPlay),
    path('updateDog', views.updateDogPlay),
    path('dogTodayPlay', views.getDogTodayPlay),
]
