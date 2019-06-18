from django.urls import path
from . import views

urlpatterns = [
    path('/update', views.updateCatPlay),
    path('', views.getCatPlay)
]
