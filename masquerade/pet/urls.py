from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_pet),
    path('breeds', views.get_breeds),
    path('uploadToken', views.get_pet_upload_avatar_token),
    path('setKeys', views.upload_pet_avatar_key),
    path('playDetails', views.get_play_details),

    # around
    path('around', views.getAroundPets),
]