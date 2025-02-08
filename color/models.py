# color/models.py
from django.db import models
from django.contrib.auth.models import User

class ColorExtraction(models.Model):
    # 인증되지 않은 사용자도 사용할 수 있도록 null=True, blank=True 설정
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/')
    extracted_color = models.CharField(max_length=7, blank=True)  # HEX 색상 코드 예: "#FBF5DD"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Extraction #{self.id} - {self.extracted_color}"
