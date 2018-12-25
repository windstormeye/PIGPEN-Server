from django.urls import path
from . import views

urlpatterns = [
    path('createPet', views.create_pet),
    path('breeds', views.get_breeds),
    path('uploadToken', views.get_pet_upload_avatar_token),
]