from django.urls import path
from . import views

urlpatterns = [
    path('run-selenium/', views.run_selenium, name='run_selenium'),
]
