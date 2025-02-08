# 예: custom_palette/models.py
from django.db import models
from django.contrib.auth.models import User

class CustomPalette(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_palettes')
    name = models.CharField(max_length=255)
    colors = models.JSONField(help_text="예: ['#FBF5DD', '#123456', '#ABCDEF']")  # 색상 목록을 JSON 배열 형태로 저장
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"
