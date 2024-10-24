from django.urls import path
from . import views

urlpatterns = [
    path('search-query/', views.run_medicare_search, name='run_selenium'),
]
