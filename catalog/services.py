from django.core.cache import cache
from .models import Product

class ProductService:
    @staticmethod
    def get_products_by_category(category_id):
        """Возвращает список всех продуктов в указанной категории с кэшированием."""
        cache_key = f'products_in_category_{category_id}'
        products = cache.get(cache_key)

        if products is None:
            products = Product.objects.filter(category_id=category_id)
            cache.set(cache_key, products, 60 * 15)  # Кешируем на 15 минут

        return products
