# 예: custom_palette/serializers.py
from rest_framework import serializers
from .models import CustomPalette

class CustomPaletteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = CustomPalette
        fields = ['id', 'user', 'name', 'colors', 'description', 'created_at']
