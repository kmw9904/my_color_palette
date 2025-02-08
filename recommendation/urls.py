# recommendation/urls.py
from django.urls import path
from .views import RecommendationView, PaletteRecommendationView

urlpatterns = [
    path('match/', RecommendationView.as_view(), name='recommendation-match'),
    path('palette/', PaletteRecommendationView.as_view(), name='palette-recommendation'),
]
