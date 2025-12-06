import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
from django.core.cache import cache
from django.db.models import QuerySet, Count, Avg, Max, Min, Q
from .models import Product, Category


class CatalogCache:
    """Менеджер кэширования для каталога"""

    # Ключи и TTL
    KEYS = {
        'products_all': ('products:all', 300),
        'products_category': ('products:category:{slug}', 300),
        'categories_all': ('categories:all', 3600),
        'category_detail': ('category:detail:{slug}', 3600),
        'product_stats': ('products:stats', 1800),
        'product_detail': ('product:detail:{id}', 600),
    }

    # 1️⃣ Сначала вспомогательные методы
    @classmethod
    def _key(cls, key_name: str, **params) -> str:
        """Генерация ключа кэша"""
        if key_name not in cls.KEYS:
            # Создаем ключ по умолчанию
            param_hash = hashlib.md5(str(params).encode()).hexdigest()[:8]
            return f"{key_name}:{param_hash}"

        key_template, _ = cls.KEYS[key_name]
        if params:
            return key_template.format(**params)
        return key_template

    @classmethod
    def _ttl(cls, key_name: str) -> int:
        """Получение TTL для ключа"""
        if key_name in cls.KEYS:
            return cls.KEYS[key_name][1]
        return 300  # По умолчанию 5 минут

    @classmethod
    def _cache_query(cls, key: str, queryset: QuerySet) -> QuerySet:
        """Кэширование QuerySet"""
        cached = cache.get(key)
        if cached:
            return cls._restore_queryset(queryset.model, cached['ids'])

        result = list(queryset)

        # Определяем TTL
        timeout = 300  # По умолчанию
        for key_name, (key_template, ttl) in cls.KEYS.items():
            if key == key_template or key.startswith(key_template.split('{')[0]):
                timeout = ttl
                break

        cache.set(key, {'ids': [obj.id for obj in result]}, timeout)
        return queryset

    @staticmethod
    def _restore_queryset(model, ids: List[int]) -> QuerySet:
        """Восстановление QuerySet из кэша"""
        objects = model.objects.filter(id__in=ids)
        obj_dict = {obj.id: obj for obj in objects}
        ordered = [obj_dict[i] for i in ids if i in obj_dict]

        qs = QuerySet(model=model)
        qs._result_cache = ordered
        qs._prefetch_done = True
        return qs

    # 2️⃣ Затем основные публичные методы
    @classmethod
    def get_products(cls, category_slug: str = None) -> QuerySet:
        """Получить продукты (все или по категории)"""
        if category_slug:
            key = cls._key('products_category', slug=category_slug)
            qs = Product.objects.filter(
                category__slug=category_slug,
                is_published=True
            )
        else:
            key = cls._key('products_all')
            qs = Product.objects.filter(is_published=True)

        return cls._cache_query(key, qs.select_related('category', 'owner'))

    @classmethod
    def get_categories(cls) -> QuerySet:
        """Получить все категории"""
        return cls._cache_query(
            cls._key('categories_all'),
            Category.objects.all().order_by('name')
        )

    @classmethod
    def get_category_info(cls, slug: str) -> Optional[Dict]:
        """Получить информацию о категории"""
        key = cls._key('category_detail', slug=slug)
        cached = cache.get(key)
        if cached:
            return cached

        try:
            category = Category.objects.get(slug=slug)
            products = Product.objects.filter(category=category, is_published=True)

            info = {
                'category': category,
                'stats': products.aggregate(
                    count=Count('id'),
                    avg_price=Avg('price'),
                    max_price=Max('price'),
                    min_price=Min('price')
                ),
                'recent': list(products.select_related('owner')[:5]),
            }
            cache.set(key, info, cls._ttl('category_detail'))
            return info
        except Category.DoesNotExist:
            return None

    @classmethod
    def get_product_info(cls, product_id: int) -> Optional[Dict]:
        """Получить информацию о продукте"""
        key = cls._key('product_detail', id=product_id)
        cached = cache.get(key)
        if cached:
            return cached

        try:
            product = Product.objects.select_related('category', 'owner').get(
                id=product_id, is_published=True
            )
            cache.set(key, product, cls._ttl('product_detail'))
            return product
        except Product.DoesNotExist:
            return None

    @classmethod
    def get_stats(cls) -> Dict:
        """Получить статистику"""
        key = cls._key('product_stats')
        cached = cache.get(key)
        if cached:
            return cached

        stats = {
            'overall': Product.objects.filter(is_published=True).aggregate(
                total=Count('id'),
                avg_price=Avg('price'),
                categories=Count('category', distinct=True),
            ),
            'categories': list(
                Category.objects.annotate(
                    count=Count('product', filter=Q(product__is_published=True))
                ).order_by('-count')[:5]
            ),
        }
        cache.set(key, stats, cls._ttl('product_stats'))
        return stats

    # 3️⃣ Методы инвалидации кэша
    @classmethod
    def invalidate_product(cls, product_id: int = None):
            """Сбросить кэш продуктов"""
            if product_id:
                cache.delete(cls._key('product_detail', id=product_id))
            cache.delete(cls._key('products_all'))
            cache.delete(cls._key('product_stats'))

    @classmethod
    def invalidate_category(cls, slug: str = None):
        """Сбросить кэш категорий"""
        if slug:
            cache.delete(cls._key('category_detail', slug=slug))
            cache.delete(cls._key('products_category', slug=slug))
        else:
            cache.delete(cls._key('categories_all'))

    @classmethod
    def clear(cls):
        """Очистить весь кэш каталога"""
        # Просто очищаем весь кэш (простой способ)
        cache.clear()


# Экспорт синглтона
cache_manager = CatalogCache()