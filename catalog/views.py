from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_detail(request, pk):
    """
    Контроллер для отображения подробной информации о товаре.
    Принимает pk товара и возвращает полную информацию.
    """
    product = get_object_or_404(Product, pk=pk)  # 🆕 ORM-запрос с обработкой 404
    return render(request, 'catalog/product_detail.html', {'product': product})

def home(request):
    """
    Контроллер главной страницы с списком товаров.
    """
    products = Product.objects.all()[:6]  # 🆕 ORM-запрос на получение продуктов
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    """Контроллер страницы контактов."""
    return render(request, 'catalog/contacts.html')