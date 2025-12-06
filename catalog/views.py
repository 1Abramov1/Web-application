from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings

from catalog.models import Product, Category
from catalog.forms import ProductForm  # Убрал CategoryForm, если его нет
from catalog.cache import CatalogCache  # Импортируем класс, а не cache_manager

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Сохраняем существующие CBV для обратной совместимости
class HomeListView(ListView):
    """Главная страница (CBV версия)"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Используем кэширование через cache_manager
        return cache_manager.get_products()[:12]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = cache_manager.get_categories()
        return context


class ProductListView(ListView):
    """Список продуктов (CBV версия)"""
    model = Product
    template_name = 'catalog/product_list_cbv.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return cache_manager.get_products()


class ProductDetailView(DetailView):
    """Детальная страница продукта (CBV версия)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product_id = self.kwargs['pk']
        # Пытаемся получить из кэша
        cached = cache_manager.get_product_info(product_id)
        if cached:
            return cached
        return get_object_or_404(Product, pk=product_id)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта (CBV версия)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # Инвалидируем кэш
        cache_manager.invalidate_product(self.object.id)
        messages.success(self.request, f'✅ Продукт "{self.object.name}" создан!')
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование продукта (CBV версия)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        product = self.get_object()
        return self.request.user.is_superuser or product.owner == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # Инвалидируем кэш
        cache_manager.invalidate_product(self.object.id)
        messages.success(self.request, f'✅ Продукт "{self.object.name}" обновлен!')
        return response


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта (CBV версия)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user.is_superuser or product.owner == self.request.user

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        # Инвалидируем кэш перед удалением
        cache_manager.invalidate_product(product.id)
        messages.success(request, f'✅ Продукт "{product.name}" удален!')
        return super().delete(request, *args, **kwargs)


class ContactsTemplateView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'


# Функции для управления публикацией (для обратной совместимости)
def unpublish_product(request, pk):
    """Снять с публикации (старая версия)"""
    return toggle_publish_status(request, pk)


def publish_product(request, pk):
    """Опубликовать (старая версия)"""
    return toggle_publish_status(request, pk)

# Создаем экземпляр для использования (если у вас cache_manager был экземпляром)
cache_manager = CatalogCache()


# Основные представления
def index(request):
    """Главная страница"""
    context = {
        'title': 'Главная страница',
        'featured_products': cache_manager.get_products()[:8] if cache_manager.get_products() else [],
        'categories': cache_manager.get_categories(),
        'stats': cache_manager.get_stats(),
    }
    return render(request, 'catalog/index.html', context)


def product_list(request):
    """Список всех продуктов"""
    products = cache_manager.get_products()

    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Все продукты',
        'products': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'catalog/product_list.html', context)


def category_products(request, slug):
    """Продукты по категории"""
    # Получаем продукты через кэш
    products = cache_manager.get_products(slug)

    # Получаем информацию о категории через кэш
    category_info = cache_manager.get_category_info(slug)

    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category_name = category_info['category'].name if category_info and 'category' in category_info else slug

    context = {
        'title': f'Продукты категории: {category_name}',
        'products': page_obj,
        'page_obj': page_obj,
        'category': category_info['category'] if category_info else None,
        'category_stats': category_info.get('stats') if category_info else None,
    }
    return render(request, 'catalog/category_products.html', context)


def product_detail(request, pk):
    """Детальная информация о продукте"""
    # Сначала пытаемся получить из кэша
    product_info = cache_manager.get_product_info(pk)

    if product_info:
        # Если есть в кэше - используем его
        context = {
            'title': product_info.name if hasattr(product_info, 'name') else 'Продукт',
            'product': product_info,
            'from_cache': True,
        }
    else:
        # Если нет в кэше - получаем из БД
        product = get_object_or_404(Product, pk=pk, is_published=True)
        context = {
            'title': product.name,
            'product': product,
            'from_cache': False,
        }

    return render(request, 'catalog/product_detail.html', context)


# CRUD операции для продуктов
@login_required
def product_create(request):
    """Создание нового продукта"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()

            messages.success(request, f'✅ Продукт "{product.name}" успешно создан!')

            # Инвалидируем кэш
            cache_manager.invalidate_product(product.id)

            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm()

    context = {
        'title': 'Создать продукт',
        'form': form,
    }
    return render(request, 'catalog/product_form.html', context)


@login_required
def product_update(request, pk):
    """Редактирование продукта"""
    product = get_object_or_404(Product, pk=pk)

    # Проверка прав
    if not request.user.is_superuser and product.owner != request.user:
        messages.error(request, '❌ У вас нет прав для редактирования этого продукта!')
        return redirect('catalog:product_detail', pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()

            messages.success(request, f'✅ Продукт "{product.name}" успешно обновлен!')

            # Инвалидируем кэш
            cache_manager.invalidate_product(product.id)

            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        'title': f'Редактировать: {product.name}',
        'form': form,
        'product': product,
    }
    return render(request, 'catalog/product_form.html', context)


@login_required
def product_delete(request, pk):
    """Удаление продукта"""
    product = get_object_or_404(Product, pk=pk)

    # Проверка прав
    if not request.user.is_superuser and product.owner != request.user:
        messages.error(request, '❌ У вас нет прав для удаления этого продукта!')
        return redirect('catalog:product_detail', pk=pk)

    if request.method == 'POST':
        product_name = product.name

        # Инвалидируем кэш перед удалением
        cache_manager.invalidate_product(product.id)

        product.delete()

        messages.success(request, f'✅ Продукт "{product_name}" успешно удален!')
        return redirect('catalog:product_list')

    context = {
        'title': f'Удалить продукт: {product.name}',
        'product': product,
    }
    return render(request, 'catalog/product_confirm_delete.html', context)


@permission_required('catalog.can_change_publish_status')
def toggle_publish_status(request, pk):
    """Переключение статуса публикации"""
    product = get_object_or_404(Product, pk=pk)

    product.is_published = not product.is_published
    product.save()

    status = "опубликован" if product.is_published else "снят с публикации"
    messages.success(request, f'✅ Продукт "{product.name}" {status}!')

    # Инвалидируем кэш через cache_manager
    cache_manager.invalidate_product(product.id)

    return redirect('catalog:product_detail', pk=product.pk)


# CRUD операции для категорий
@login_required
def category_create(request):
    """Создание новой категории с проверкой slug"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            messages.error(request, '❌ Название категории обязательно!')
            return render(request, 'catalog/category_form.html', {
                'title': 'Создать категорию',
                'name': name,
                'description': description,
            })

        try:
            # Создаем категорию
            category = Category(
                name=name,
                description=description
            )
            # Сохраняем (сгенерируется slug)
            category.save()

            messages.success(request, f'✅ Категория "{category.name}" создана!')

            # Инвалидируем кэш
            cache_manager.invalidate_category()

            # Проверяем есть ли slug перед редиректом
            if category.slug:
                return redirect('catalog:category_products', slug=category.slug)
            else:
                # Если slug пустой, идем в список категорий
                return redirect('catalog:categories_list')

        except Exception as e:
            messages.error(request, f'❌ Ошибка: {str(e)}')
            return render(request, 'catalog/category_form.html', {
                'title': 'Создать категорию',
                'name': name,
                'description': description,
                'error': str(e),
            })

    # GET запрос
    return render(request, 'catalog/category_form.html', {
        'title': 'Создать категорию',
    })


@login_required
def category_update(request, slug):
    """Редактирование категории (упрощенная версия)"""
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        old_slug = category.slug

        category.name = request.POST.get('name', category.name)
        category.description = request.POST.get('description', category.description)
        category.save()

        messages.success(request, f'✅ Категория "{category.name}" успешно обновлена!')

        # Инвалидируем кэш для старого и нового slug
        cache_manager.invalidate_category(old_slug)
        cache_manager.invalidate_category(category.slug)

        return redirect('catalog:category_products', slug=category.slug)

    context = {
        'title': f'Редактировать категорию: {category.name}',
        'category': category,
    }
    return render(request, 'catalog/category_form.html', context)


@login_required
def category_delete(request, slug):
    """Удаление категории"""
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        category_name = category.name

        # Инвалидируем кэш перед удалением
        cache_manager.invalidate_category(category.slug)

        category.delete()

        messages.success(request, f'✅ Категория "{category_name}" успешно удалена!')
        return redirect('catalog:product_list')

    context = {
        'title': f'Удалить категорию: {category.name}',
        'category': category,
    }
    return render(request, 'catalog/category_confirm_delete.html', context)


# Вспомогательные представления
def categories_list(request):
    """Список всех категорий"""
    categories = cache_manager.get_categories()

    context = {
        'title': 'Все категории',
        'categories': categories,
        'from_cache': hasattr(categories, '_result_cache'),
    }
    return render(request, 'catalog/categories_list.html', context)


def search_products(request):
    """Поиск продуктов"""
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')

    if query or category_slug:
        # Получаем базовый QuerySet из кэша
        if category_slug:
            products = list(cache_manager.get_products(category_slug))
        else:
            products = list(cache_manager.get_products())

        # Применяем поиск по названию
        if query:
            products = [p for p in products if query.lower() in p.name.lower()]

        # Пагинация
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'title': f'Результаты поиска: {query}',
            'products': page_obj,
            'page_obj': page_obj,
            'query': query,
            'category_slug': category_slug,
        }
        return render(request, 'catalog/search_results.html', context)

    return redirect('catalog:product_list')


# Статистика и отчеты
@login_required
def statistics_view(request):
    """Страница статистики"""
    stats = cache_manager.get_stats()

    context = {
        'title': 'Статистика магазина',
        'overall_stats': stats.get('overall', {}),
        'popular_categories': stats.get('categories', []),
        'from_cache': 'timestamp' in stats,
    }
    return render(request, 'catalog/statistics.html', context)


# Утилиты для кэширования (оставлены для обратной совместимости)
def clear_product_cache(product_id):
    """Очистка кэша для продукта (совместимость)"""
    cache_manager.invalidate_product(product_id)


def clear_product_list_cache():
    """Очистка кэша списка продуктов (совместимость)"""
    cache_manager.invalidate_product()


def get_cached_product_list():
    """Получение списка продуктов из кэша или БД (совместимость)"""
    return cache_manager.get_products()


# Дополнительная функция для проверки работы кэша
@login_required
def cache_debug(request):
    """Страница отладки кэша"""
    from django.core.cache import cache as django_cache

    # Создаем ключи вручную (так как знаем шаблоны)
    cache_keys = {
        'products_all': 'products:all',
        'categories_all': 'categories:all',
        'product_stats': 'products:stats',
    }

    cache_info = {}
    for key_name, key_template in cache_keys.items():
        cache_info[f'{key_name}_in_cache'] = bool(django_cache.get(key_template))

    # Тестируем работу кэша
    test_results = {
        'products_count': len(list(cache_manager.get_products())),
        'categories_count': len(list(cache_manager.get_categories())),
        'stats_loaded': 'timestamp' in cache_manager.get_stats(),
    }

    context = {
        'title': 'Отладка кэша',
        'cache_info': cache_info,
        'test_results': test_results,
        'cache_enabled': getattr(settings, 'CACHE_ENABLED', True),
    }

    return render(request, 'catalog/cache_debug.html', context)