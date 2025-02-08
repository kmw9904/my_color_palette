# color/urls.py
from django.urls import path
from .views import ColorExtractionView

urlpatterns = [
    path('extract/', ColorExtractionView.as_view(), name='color-extraction'),
]
