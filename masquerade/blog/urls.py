from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('createBlog', views.create_blog, name='create_masuser'),
    path('deleteBlog', views.delete_blog, name='delete_blog'),
]