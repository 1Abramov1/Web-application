from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import QuerySet
from .models import Product
from .forms import ProductForm


class HomeListView(ListView):
    """
    CBV для главной страницы со списком товаров.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet:
        # Показываем только опубликованные товары на главной
        return Product.objects.filter(is_published=True)[:6]


class ContactsTemplateView(TemplateView):
    """
    CBV для страницы контактов.
    """
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    """CBV для списка продуктов."""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """CBV для детального просмотра продукта."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def form_valid(self, form):
        """🆕 Автоматически устанавливаем владельца при создании"""
        form.instance.owner = self.request.user
        messages.success(self.request, '✅ Продукт успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """CBV для редактирования продукта с проверкой владельца."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def test_func(self):
        """🆕 Проверяем, что пользователь - владелец продукта"""
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        """🆕 Обработка отсутствия прав"""
        messages.error(self.request, '❌ Вы можете редактировать только свои продукты!')
        return redirect('catalog:product_list')

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, '✅ Продукт успешно обновлен!')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """CBV для удаления продукта с проверкой прав."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def test_func(self):
        """🆕 Проверяем, что пользователь - владелец ИЛИ модератор"""
        product = self.get_object()
        user = self.request.user

        # Владелец может удалять свои продукты
        if user == product.owner:
            return True

        # Модератор может удалять любые продукты
        if user.has_perm('catalog.delete_product'):
            return True

        return False

    def handle_no_permission(self):
        """🆕 Обработка отсутствия прав"""
        product = self.get_object()
        if self.request.user == product.owner:
            messages.error(self.request, '❌ У вас нет прав для удаления продуктов!')
        else:
            messages.error(self.request, '❌ Вы можете удалять только свои продукты!')
        return redirect('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        """Добавляем сообщение об успешном удалении"""
        messages.success(self.request, '✅ Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


# 🆕 Функции для управления публикацией

@permission_required('catalog.can_unpublish_product')
def unpublish_product(request, pk):
    """Отмена публикации продукта"""
    product = get_object_or_404(Product, pk=pk)

    if product.is_published:
        product.is_published = False
        product.save()
        messages.success(request, f'✅ Публикация продукта "{product.name}" отменена!')
    else:
        messages.warning(request, f'ℹ️ Продукт "{product.name}" уже не опубликован')

    return redirect('catalog:product_detail', pk=product.pk)


@permission_required('catalog.can_change_publish_status')
def publish_product(request, pk):
    """Публикация продукта"""
    product = get_object_or_404(Product, pk=pk)

    if not product.is_published:
        product.is_published = True
        product.save()
        messages.success(request, f'✅ Продукт "{product.name}" опубликован!')
    else:
        messages.warning(request, f'ℹ️ Продукт "{product.name}" уже опубликован')

    return redirect('catalog:product_detail', pk=product.pk)


@permission_required('catalog.can_change_publish_status')
def toggle_publish_status(request, pk):
    """Переключение статуса публикации"""
    product = get_object_or_404(Product, pk=pk)

    product.is_published = not product.is_published
    product.save()

    status = "опубликован" if product.is_published else "снят с публикации"
    messages.success(request, f'✅ Продукт "{product.name}" {status}!')

    return redirect('catalog:product_detail', pk=product.pk)