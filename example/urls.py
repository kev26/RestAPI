"""ThoDia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from asyncio import base_events
from atexit import register
from email.mime import base
from django.contrib import admin
from django.db import router
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from sellHouse import views
from rest_framework.urlpatterns import format_suffix_patterns


# Create default router and register our viewset
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'apartments', views.ApartmentViewset, basename='apartment')
router.register(r'solds', views.SoldViewSet, basename='sold')
router.register(r'transactions', views.TransactionViewset,
                basename='transaction')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # Authentication by Djoser
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
