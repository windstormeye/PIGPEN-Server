from django.urls import path
from . import views

urlpatterns = [
    path('createmasuser', views.create_masuser, name='create_masuser'),
    path('login', views.login, name='masuser_login'),
    path('logout', views.logout, name='masuser_logout'),
    path('update', views.update_user, name='update_masuser'),
]