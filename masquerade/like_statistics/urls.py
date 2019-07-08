from django.urls import path
from . import views

urlpatterns = [
    path('', views.like_change),
    path('getLikeBlogs', views.get_like_blog),
]
