# color/serializers.py
from rest_framework import serializers
from .models import ColorExtraction

class ColorExtractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorExtraction
        fields = ['id', 'user', 'image', 'extracted_color', 'created_at']
        read_only_fields = ['extracted_color', 'created_at']
