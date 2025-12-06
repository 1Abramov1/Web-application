from django.db.models import QuerySet, Count, Q
from django.shortcuts import get_object_or_404
from .models import Product, Category


def get_products_by_category(category_slug: str = None) -> QuerySet:
    """
    Функция для получения продуктов по категории.
    """
    products = Product.objects.filter(is_published=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return products.select_related('category', 'owner')


def get_categories_with_counts():
    """
    Получить все категории с подсчетом количества продуктов.
    """
    from django.db.models import Count, Q

    # Фильтруем только категории с slug
    categories = Category.objects.filter(
        slug__isnull=False
    ).exclude(
        slug=''
    ).annotate(
        products_count=Count('product', filter=Q(product__is_published=True))
    ).order_by('name')

    return categories


def get_category_info(slug: str):
    """
    Получить информацию о категории.
    """
    try:
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(
            category=category,
            is_published=True
        ).select_related('owner')
        return {
            'category': category,
            'products': products,
            'count': products.count()
        }
    except Category.DoesNotExist:
        return None


# Дополнительные функции (опционально)
def get_all_categories():
    """
    Получить все категории.
    """
    return Category.objects.all()


def get_popular_products(limit: int = 6):
    """
    Получить популярные продукты.
    """
    return Product.objects.filter(
        is_published=True).order_by('-created_at')[:limit]