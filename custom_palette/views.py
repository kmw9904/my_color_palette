# 예: custom_palette/views.py
from rest_framework import viewsets, permissions
from .models import CustomPalette
from .serializers import CustomPaletteSerializer

class CustomPaletteViewSet(viewsets.ModelViewSet):
    queryset = CustomPalette.objects.all().order_by('-created_at')
    serializer_class = CustomPaletteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
