# 예: custom_palette/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomPaletteViewSet

router = DefaultRouter()
router.register(r'palettes', CustomPaletteViewSet, basename='custompalette')

urlpatterns = [
    path('', include(router.urls)),
]
