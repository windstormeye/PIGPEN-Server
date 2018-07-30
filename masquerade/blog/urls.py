from django.urls import path
from . import views

urlpatterns = [
    path('createBlog', views.create_blog, name='create_masuser'),

]