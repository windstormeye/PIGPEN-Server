from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('masuser/', include('user.urls')),
    path('blog/', include('blog.urls')),
    path('comment/', include('comment.urls')),
    path('like/', include('like_statistics.urls')),
    path('realPet/', include('pet.urls')),
    path('virtualPet/', include('virtual_pet.urls')),
    path('petDrink/', include('pet_drink.urls')),
    path('friend/', include('friend.urls')),
]
