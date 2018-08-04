from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_avatar, name='upload_avatar'),
    path('update', views.update_avatar, name='update_avatar'),
]
