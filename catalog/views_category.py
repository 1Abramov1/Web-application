from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .services import get_products_by_category, get_categories_with_counts


class CategoryProductsView(ListView):
    """
    Представление для отображения продуктов по категории.
    """
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Получаем продукты по категории"""
        category_slug = self.kwargs.get('category_slug')
        return get_products_by_category(category_slug)

    def get_context_data(self, **kwargs):
        """Добавляем информацию о категории в контекст"""
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
            context['title'] = f'Товары в категории: {context["category"].name}'
        else:
            context['category'] = None
            context['title'] = 'Все товары'

        context['categories'] = get_categories_with_counts()
        context['products_count'] = context['products'].count()

        return context


def category_products_simple(request, category_slug=None):
    """
    Простое представление для отображения продуктов по категории.
    """
    products = get_products_by_category(category_slug)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        title = f'Товары в категории: {category.name}'
    else:
        title = 'Все товары'

    categories = get_categories_with_counts()

    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'title': title,
        'products_count': products.count(),
    }

    return render(request, 'catalog/category_products.html', context)