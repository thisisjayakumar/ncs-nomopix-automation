from django.urls import path
from . import views

urlpatterns = [
    path('search-query/', views.MedicareSearchView.as_view(), name='run_selenium'),
]
