from django.urls import path
from django.shortcuts import redirect
from .views import (
    HomeListView, ContactsTemplateView,
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    toggle_publish_status,
)
from . import views as catalog_views

app_name = 'catalog'

urlpatterns = [
    # Основные маршруты (CBV)
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),

    # Продукты (CBV)
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Категории (функциональные с кэшем)
    path('categories/', catalog_views.categories_list, name='categories_list'),
    path('category/create/', catalog_views.category_create, name='category_create'),
    path('category/<slug:slug>/', catalog_views.category_products, name='category_products'),
    path('category/<slug:slug>/update/', catalog_views.category_update, name='category_update'),
    path('category/<slug:slug>/delete/', catalog_views.category_delete, name='category_delete'),

    # 📌 Для header.html (псевдоним) - ДУБЛИРУЕТ categories_list
    path('category/', catalog_views.categories_list, name='category_products_all'),

    # Поиск и статистика (функциональные)
    path('search/', catalog_views.search_products, name='search_products'),
    path('statistics/', catalog_views.statistics_view, name='statistics'),

    # Управление публикацией
    path('product/<int:pk>/toggle-publish/', toggle_publish_status,
         name='product_toggle_publish'),
]