from django.urls import path
from . import views

urlpatterns = [
    path('', views.getFriend),
    path('add', views.addFriend),
    path('search', views.searchFriend),
]
