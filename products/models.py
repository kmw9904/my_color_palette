from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('아우터', '아우터'),
        ('상의', '상의'),
        ('하의', '하의'),
        ('악세서리', '악세서리'),
        # 필요한 다른 카테고리도 추가
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.CharField(max_length=50)  # 가격은 텍스트로 저장할 수도 있고, 정수로 변환할 수도 있음
    image_url = models.URLField()
    # 상품 이미지의 대표 색상을 저장하고 싶다면 (추출 로직이 있다면)
    color_hex = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} ({self.category})"
