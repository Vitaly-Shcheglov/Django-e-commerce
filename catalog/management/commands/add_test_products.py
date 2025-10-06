from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Добавляет тестовые продукты"

    def handle(self, *args, **options):
        Product.objects.all().delete()  # удаляем старые продукты
        Category.objects.all().delete()  # удаляем старые категории
        category = Category.objects.create(
            name="Тестовая категория", description="Описание тестовой категории"
        )  # Создаем новую категорию
        Product.objects.create(
            name="Новый продукт",
            description="Описание нового продукта",
            image="path/to/image.jpg",
            category=category,
            price=200.00,
        )  # Добавляем новые продукты
