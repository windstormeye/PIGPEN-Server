from django.urls import path
from . import views

urlpatterns = [
    path('all', views.all),
    path('day', views.day),
    path('create', views.create),
    path('update', views.update),
    path('delete', views.delete),
]
