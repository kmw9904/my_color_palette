# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def index(request):
    return HttpResponse("Hello, this is the homepage of the API backend.")

urlpatterns = [
    path('', index),  # 루트 URL에 간단한 뷰 추가
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/color/', include('color.urls')),
    path('api/community/', include('community.urls')),
    path('api/recommendation/', include('recommendation.urls')),
    path('api/custom_palette/', include('custom_palette.urls')),
    
    # JWT 관련 엔드포인트
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
