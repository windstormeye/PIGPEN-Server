from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('masuser/', include('user.urls')),
    path('blog/', include('blog.urls')),
    path('comment/', include('comment.urls')),
    path('like/', include('like_statistics.urls')),
    path('pet/', include('pet.urls')),
    path('petDrink/', include('pet_drink.urls')),
    path('friend/', include('friend.urls')),
    path('play/', include('play.urls')),
    path('drink/', include('drink.urls')),
    path('score/', include('score.urls')),
    path('eat/', include('eat.urls')),
    path('collect/', include('collect_statistics.urls')),
]
