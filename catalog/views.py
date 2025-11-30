from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
        return Product.objects.all()[:6]


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

    # Опционально: настройка перенаправления для неавторизованных
    login_url = '/users/login/'
    redirect_field_name = 'next'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для удаления продукта."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    redirect_field_name = 'next'