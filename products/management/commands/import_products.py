# products/management/commands/import_products.py

import csv
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file.')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        # 파일이 탭 구분되어 있다고 가정
        with open(csv_file, encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter="\t")
            count = 0
            for row in reader:
                category = row.get("카테고리")
                # 만약 카테고리 값이 없으면 해당 행을 건너뜁니다.
                if not category:
                    self.stdout.write(self.style.WARNING("Skipping row with missing category: " + str(row)))
                    continue

                Product.objects.create(
                    category=category,
                    product_name=row.get("상품명"),
                    brand=row.get("브랜드명"),
                    price=row.get("가격"),
                    image_url=row.get("이미지_URL")
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f"Imported {count} products."))
