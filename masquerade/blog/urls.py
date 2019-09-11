from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list),
    path('create', views.create_blog),
    path('delete', views.delete_blog),
    path('details', views.blog_details),
    path('petAll', views.get_pet_blog)
]
