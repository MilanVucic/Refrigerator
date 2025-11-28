"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework import routers
from fridge.views import FridgeViewSet, ItemViewSet

router = routers.DefaultRouter()
router.register("fridges", FridgeViewSet)
router.register("items", ItemViewSet)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Api routes
    path("api/", include(router.urls)),

    # Account management routes (login/register/refresh)
    path("api/accounts/", include("accounts.urls")),
]

