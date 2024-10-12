from django.urls import path
from . import views

urlpatterns = [
    path('create-user/', views.CreateUser, name='create_user'),
]
