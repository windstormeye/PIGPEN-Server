from django.urls import path
from . import views

urlpatterns = [
    path('', views.get),
    path('create', views.post),
]
