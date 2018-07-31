from django.urls import path
from . import views

urlpatterns = [
    path('createComment', views.create_comment, name='create_comment'),
    path('getComment', views.get_comment, name='get_comment'),
]
