from django.urls import path
from . import views

urlpatterns = [
    path('createmasuser', views.create_masuser),
    path('login', views.login),
    path('logout', views.logout),
    path('update', views.update_user),
    path('updateToken', views.update_token),
    path('getUserDetails', views.get_user_details),
    path('checkPhone', views.check_phone),
    path('pets', views.get_user_pet_info),
    path('getRCToken', views.getRCToken),
]