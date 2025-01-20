"""
URL configuration for cgsmedicare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import *
from selenium_headless_browser.views import CancelTestsView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'admin/feedbacks', FeedbackAdminViewSet, basename='admin-feedback')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('api/v1/', include([
        path('', include(router.urls)),
    ])),
    path('users/', include('users.urls')),
    path('run-query/', include('selenium_headless_browser.urls')),
    path('api/v2/feedback/', FeedbackAPIView.as_view(), name='feedback-api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v2/internal/canceltests/', CancelTestsView.as_view(), name='cancel-tests'),
]

