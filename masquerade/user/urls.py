from django.urls import path
from . import views

urlpatterns = [
    path('createmasuser', views.create_masuser, name='create_masuser'),
    path('login', views.login, name='masuser_login'),
    path('logout', views.logout, name='masuser_logout'),
    path('update', views.update_user, name='update_masuser'),
    path('updateToken', views.update_token, name='update_token'),
    path('getUserDetails', views.get_user_details, name='get_user_details'),
    path('checkPhone', views.check_phone, name='check_user_phone'),
    path('pets', views.get_user_pet_info, name='get_user_pet_info'),
]